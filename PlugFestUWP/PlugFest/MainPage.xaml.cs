using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using System.Runtime.InteropServices;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Navigation;
using Windows.Devices.Bluetooth;
using Windows.Devices.Bluetooth.Rfcomm;
using Windows.Devices.Enumeration;
using Windows.Storage.Streams;
using Windows.Networking.Sockets;
using MQTTnet;
using MQTTnet.Server;
using MQTTnet.Client;
using MQTTnet.Adapter;
using MQTTnet.Diagnostics;
using MQTTnet.Protocol;
using System.Diagnostics;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System.Collections.ObjectModel;
using System.Threading;
using Windows.Devices.SerialCommunication;

namespace PlugFest
{
    /// <summary>
    /// Current design of topics: 
    /// "PlugFest/sensors/[Sensor Name]/TEDS"
    /// "PlugFest/sensors/[Sensor Name]/data"
    /// "PlugFest/sensors/[Sensor Name]/integrated"
    /// </summary>
    public sealed partial class MainPage : Page
    {
        public bool IsServerRunning { get => isServerRunning; set => isServerRunning = value; }
        private bool isServerRunning = false;
        public bool IsBTServerRunning { get => isBTServerRunning; set => isBTServerRunning = value; }
        private bool isBTServerRunning = false;
        private IMqttServer _mqttServer = new MqttFactory().CreateMqttServer();
        private MqttServerOptionsBuilder _serverOptionBuilder;
        private IMqttClient _mqttClient = new MqttFactory().CreateMqttClient();
        private MqttClientOptionsBuilder _clientOptionBuilder;
        private StreamSocketListener _listener = new StreamSocketListener();
        private RfcommServiceProvider _provider;
        private StreamSocket _socket;
        private RetainedMessageHandler retainStorage = new RetainedMessageHandler();
        private DataReader dataReaderObject;
        private ObservableCollection<PairedDeviceInfo> _pairedDevices;
        // [DllImport("operateTEDS", CharSet=CharSet.Unicode)]
        // private static extern String TEDStoString(); 

        public MainPage()
        {
            this.InitializeComponent();
            Debug.WriteLine(retainStorage.TEDSStringA);
            this.DataContext = retainStorage;
            // UWP won't allow you to bind loopback addr.
            // bindAddr = System.Net.IPAddress.Parse("127.0.0.1");
            // bindAddr = System.Net.IPAddress.Parse("192.168.56.1");
            _serverOptionBuilder = new MqttServerOptionsBuilder()
                .WithConnectionBacklog(100)
                .WithStorage(retainStorage)
                //.WithDefaultEndpointBoundIPAddress(bindAddr)
                .WithDefaultEndpointPort(1883);
            _clientOptionBuilder = new MqttClientOptionsBuilder()
                .WithClientId("Client1")
                .WithTcpServer("127.0.0.1")
                .WithCleanSession();
            AsignMQTTCallback();
            AsignBluetoothCallback();
        }

        private void AsignMQTTCallback()
        {
            _mqttServer.ApplicationMessageReceived += MqttServer_ApplicationMessageReceived;
            _mqttServer.ClientConnected += MqttServer_ClientConnected;
            _mqttServer.ClientDisconnected += MqttServer_ClientDisconnected;
            // Looks like it is confricting with the disconnectAsync
            // _mqttClient.Disconnected += ConnectionErrorHandle;
        }

        private void AsignBluetoothCallback()
        {
            _listener.ConnectionReceived += OnBTConnectionReceived;
        }


        private async void TEDS_TextChanged(object sender, RoutedEventArgs e)
        {
            retainStorage.UpdateTEDS();
            await PublishTEDS();
        }

        private async Task PublishTEDS()
        {
            if (_mqttClient.IsConnected)
            {
                foreach (var message in retainStorage.GetRetainList())
                {
                    await _mqttClient.PublishAsync(message);
                }
            }
        }

        private async void StartServer(object sender, RoutedEventArgs e)
        {
            if (!IsServerRunning)
            {
                try
                {
                    IsServerRunning = true;
                    await _mqttServer.StartAsync(_serverOptionBuilder.Build());
                    Debug.WriteLine("Server started.");
                    await ConnectClient();
                    await PublishTEDS();
                }
                catch (Exception ex)
                {
                    Debug.WriteLine("Error on server start." + ex.ToString());
                    throw;
                }
            }
            else
            {
                Debug.WriteLine("Server is already running.");
            }
        }

        private async void StopServer(object sender, RoutedEventArgs e)
        {
            if (IsServerRunning)
            {
                try
                {
                    await _mqttServer.StopAsync();
                    IsServerRunning = false;
                    Debug.WriteLine("Server stoped.");
                }
                catch (Exception ex)
                {
                    Debug.WriteLine("Error on server shutdown." + ex.ToString());
                    throw;
                }

            }
        }
        private async void ReinitializeRetainMessage(object sender, RoutedEventArgs e)
        {
            Debug.WriteLine("Reinitializing retained messages. It'll be droped unless it is predefined TEDS.");
            await _mqttServer.ClearRetainedMessagesAsync();
            await PublishTEDS();
        }


        private static void MqttServer_ClientConnected(object sender, MQTTnet.Server.MqttClientConnectedEventArgs e)
        {
            Debug.WriteLine($"Client[{e.ClientId}] connected");
        }

        private static void MqttServer_ClientDisconnected(object sender, MQTTnet.Server.MqttClientDisconnectedEventArgs e)
        {
            Debug.WriteLine($"Client[{e.ClientId}] disconnected！");
        }

        private static void MqttServer_ApplicationMessageReceived(object sender, MqttApplicationMessageReceivedEventArgs e)
        {
            Debug.WriteLine($"Client[{e.ClientId}]>> Topic：{e.ApplicationMessage.Topic} Payload：{Encoding.UTF8.GetString(e.ApplicationMessage.Payload)} Qos：{e.ApplicationMessage.QualityOfServiceLevel} Re：{e.ApplicationMessage.Retain}");
        }

        // Bluetooth functions

        async Task InitializeRfcommDeviceService()
        {
            try
            {
                DeviceInformationCollection DeviceInfoCollection = await DeviceInformation.FindAllAsync(RfcommDeviceService.GetDeviceSelector(RfcommServiceId.SerialPort));


                var numDevices = DeviceInfoCollection.Count();

                _pairedDevices = new ObservableCollection<PairedDeviceInfo>();
                _pairedDevices.Clear();

                if (numDevices == 0)
                {
                    System.Diagnostics.Debug.WriteLine("InitializeRfcommDeviceService: No paired devices found.");
                }
                else
                {
                    // Found paired devices.
                    foreach (var deviceInfo in DeviceInfoCollection)
                    {
                        _pairedDevices.Add(new PairedDeviceInfo(deviceInfo));
                    }
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine("InitializeRfcommDeviceService: " + ex.Message);
            }
        }

        private void StopBluetooth(object sender, RoutedEventArgs e)
        {
            if (isBTServerRunning)
            {
                isBTServerRunning = false;
                _socket.Dispose();
                _socket = null;
            }
        }
        private async void StartBluetooth(object sender, RoutedEventArgs e)
        {
            if (!IsBTServerRunning)
            {
                isBTServerRunning = true;
                await InitializeRfcommDeviceService();
                DeviceInformation DeviceInfo; // = await DeviceInformation.CreateFromIdAsync(this.TxtBlock_SelectedID.Text);
                DeviceInfo = _pairedDevices.First().DeviceInfo;

                bool success = true;
                try
                {
                    var _service = await RfcommDeviceService.FromIdAsync(DeviceInfo.Id);

                    if (_socket != null)
                    {
                        _socket.Dispose();
                    }

                    _socket = new StreamSocket();
                    try
                    {
                        await _socket.ConnectAsync(_service.ConnectionHostName, _service.ConnectionServiceName);
                    }
                    catch (Exception ex)
                    {
                        isBTServerRunning = false;
                        success = false;
                        System.Diagnostics.Debug.WriteLine("Connect:" + ex.Message);
                    }
                    if (success)
                    {
                        string msg = String.Format("Connected to {0}!", _socket.Information.RemoteAddress.DisplayName);
                        System.Diagnostics.Debug.WriteLine(msg);
                    }
                }
                catch (Exception ex)
                {
                    System.Diagnostics.Debug.WriteLine("Overall Connect: " + ex.Message);
                    _socket.Dispose();
                    _socket = null;
                }
                Listen();
            }
        }

        private async void Listen()
        {
            try
            {
                var ReadCancellationTokenSource = new CancellationTokenSource();
                if (_socket.InputStream != null)
                {
                    dataReaderObject = new DataReader(_socket.InputStream);
                    // keep reading the serial input
                    while (true)
                    {
                        await ReadAsync(ReadCancellationTokenSource.Token);
                    }
                }
            }
            catch (Exception ex)
            {
                isBTServerRunning = false;
                if (ex.GetType().Name == "TaskCanceledException")
                {
                    System.Diagnostics.Debug.WriteLine("Listen: Reading task was cancelled, closing device and cleaning up");
                }
                else
                {
                    System.Diagnostics.Debug.WriteLine("Listen: " + ex.Message);
                }
            }
            finally
            {
                // Cleanup once complete
                if (dataReaderObject != null)
                {
                    dataReaderObject.DetachStream();
                    dataReaderObject = null;
                }
            }
        }

        private async Task ReadAsync(CancellationToken cancellationToken)
        {
            Task<UInt32> loadAsyncTask;

            uint ReadBufferLength = 1024;

            // If task cancellation was requested, comply
            cancellationToken.ThrowIfCancellationRequested();

            // Set InputStreamOptions to complete the asynchronous read operation when one or more bytes is available
            dataReaderObject.InputStreamOptions = InputStreamOptions.Partial;

            // Create a task object to wait for data on the serialPort.InputStream
            loadAsyncTask = dataReaderObject.LoadAsync(ReadBufferLength).AsTask(cancellationToken);

            // Launch the task and wait
            UInt32 bytesRead = await loadAsyncTask;
            if (bytesRead > 0)
            {
                try
                {
                    string recvdtxt = dataReaderObject.ReadString(bytesRead);
                    System.Diagnostics.Debug.WriteLine(recvdtxt);
                    var message = new MqttApplicationMessageBuilder()
            .WithTopic("PlugFest/sensors/A/integrated")
            .WithPayload(recvdtxt)
            .WithExactlyOnceQoS()
            .Build();
                    await _mqttClient.PublishAsync(message);
                }
                catch (Exception ex)
                {
                    Debug.WriteLine("ReadAsync: " + ex.Message);
                }

            }
        }

        private async void OnBTConnectionReceived(StreamSocketListener listener, StreamSocketListenerConnectionReceivedEventArgs args)
        {
            Debug.WriteLine("recieved something");
            try
            {
                // Stop advertising/listening so that we're only serving one client
                _provider.StopAdvertising();
                listener.Dispose();
                // _socket = args.Socket;
                Debug.WriteLine("Successfully stoped listening to the sock.");
            }
            catch (Exception ex)
            {
                Debug.WriteLine("Error on BT received." + ex.ToString());
                throw;
            }

            // The client socket is connected. At this point the App can wait for
            // the user to take some action, e.g. click a button to receive a file
            // from the device, which could invoke the Picker and then save the
            // received file to the picked location. The transfer itself would use  
            // the Sockets API and not the Rfcomm API, and so is omitted here for
            // brevity.

            // use function like strchar() to find separater.
            // Create loop here to make server able to get multiple messages within one session.
            var reader = new DataReader(_socket.InputStream);
            uint sizeFieldCount = await reader.LoadAsync(sizeof(uint));
            uint size = reader.ReadUInt32();
            uint sizeFieldCount2 = await reader.LoadAsync(size);
            var str = reader.ReadString(sizeFieldCount2);
            Debug.WriteLine("server receive {0}", str);
            var message = new MqttApplicationMessageBuilder()
                        .WithTopic("MyTopic")
                        .WithPayload(str)
                        .WithExactlyOnceQoS()
                        .Build();
            await _mqttClient.PublishAsync(message);
            Debug.WriteLine("Successfuly published the message.");
        }

        private async Task ConnectClient() {
            if (!_mqttClient.IsConnected)
            {
                try
                {
                    Debug.WriteLine("Client is trying to connect to the mqtt server.");
                    await _mqttClient.ConnectAsync(_clientOptionBuilder.Build());
                }
                catch (Exception ex)
                {
                    Debug.WriteLine("Error on client connect." + ex.ToString());
                    throw;
                }
            }
            else
            {
                Debug.WriteLine("Client is already connected.");
            }
        }

        private async void ConnectClient_Click(object sender, RoutedEventArgs e)
        {
            await ConnectClient();
        }

        private async void DisconnectClient(object sender, RoutedEventArgs e)
        {
            if (_mqttClient.IsConnected)
            {
                try
                {
                    await _mqttClient.DisconnectAsync();
                    await Task.Delay(500);
                    Debug.WriteLine("Client disconnected.");
                }
                catch (Exception ex)
                {
                    Debug.WriteLine("Error on disconnecting client" + ex.ToString());
                    throw;
                }

            }
        }

        private async void PublishTestMessage(object sender, RoutedEventArgs e)
        {
            if (_mqttClient.IsConnected)
            {
                try
                {
                    var message = new MqttApplicationMessageBuilder()
                        .WithTopic("MyTopic")
                        .WithPayload("Hello World")
                        .WithExactlyOnceQoS()
                        .WithRetainFlag()
                        .Build();
                    await _mqttClient.PublishAsync(message);
                    Debug.WriteLine("Successfuly published the message.");
                }
                catch (Exception ex)
                {
                    Debug.WriteLine("Error on publishing the message." + ex.ToString());
                    throw;
                }
            }
            else
            {
                Debug.WriteLine("Client is not connected. First, check the connection to the server.");
            }
        }

        private async void ConnectionErrorHandle(object sender, MQTTnet.Client.MqttClientDisconnectedEventArgs e)
        {
            Debug.WriteLine("### DISCONNECTED FROM SERVER ###");
            await Task.Delay(TimeSpan.FromSeconds(5));
            try
            {
                await _mqttClient.ConnectAsync(_clientOptionBuilder.Build());
            }
            catch
            {
                Console.WriteLine("### RECONNECTING FAILED ###");
            }
        }

    }
}