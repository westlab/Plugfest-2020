using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
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
using Windows.Storage.Streams;

namespace PlugFest
{
    /// <summary>
    /// それ自体で使用できる空白ページまたはフレーム内に移動できる空白ページ。
    /// </summary>
    public sealed partial class MainPage : Page
    {
        private IMqttServer _mqttServer = new MqttFactory().CreateMqttServer();
        private MqttServerOptionsBuilder _serverOptionBuilder;
        private IMqttClient _mqttClient = new MqttFactory().CreateMqttClient();
        private MqttClientOptionsBuilder _clientOptionBuilder;
        private StreamSocketListener _listener = new StreamSocketListener();
        private bool isServerRunning = false;
        public bool IsServerRunning { get => isServerRunning; set => isServerRunning = value; }
        RfcommServiceProvider _provider;
        StreamSocket _socket;

        public MainPage()
        {
            this.InitializeComponent();
            // UWP won't allow you to bind loopback addr.
            // bindAddr = System.Net.IPAddress.Parse("127.0.0.1");
            // bindAddr = System.Net.IPAddress.Parse("192.168.56.1");
            _serverOptionBuilder = new MqttServerOptionsBuilder()
                .WithConnectionBacklog(100)
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
            _mqttClient.Disconnected += ConnectionErrorHandle;
        }

        private void AsignBluetoothCallback()
        {
            _listener.ConnectionReceived += OnBTConnectionReceived;
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
        private async void StartBluetooth(object sender, RoutedEventArgs e)
        {
            _provider = await RfcommServiceProvider.CreateAsync(RfcommServiceId.ObexObjectPush);
            await _listener.BindServiceNameAsync(_provider.ServiceId.AsString(), SocketProtectionLevel.BluetoothEncryptionAllowNullAuthentication);

            // Set the SDP attributes and start advertising
            InitializeServiceSdpAttributes(_provider);
            _provider.StartAdvertising(_listener);
        }

        // const uint SERVICE_VERSION_ATTRIBUTE_ID = 0x0300;
        const uint SERVICE_VERSION_ATTRIBUTE_ID = 0x47d6;
        const byte SERVICE_VERSION_ATTRIBUTE_TYPE = 0x0A;   // UINT32
        const uint SERVICE_VERSION = 200;
        void InitializeServiceSdpAttributes(RfcommServiceProvider provider)
        {
            var writer = new Windows.Storage.Streams.DataWriter();

            // First write the attribute type
            writer.WriteByte(SERVICE_VERSION_ATTRIBUTE_TYPE);
            // Then write the data
            writer.WriteUInt32(SERVICE_VERSION);

            var data = writer.DetachBuffer();
            provider.SdpRawAttributes.Add(SERVICE_VERSION_ATTRIBUTE_ID, data);
        }

        private async void OnBTConnectionReceived(StreamSocketListener listener, StreamSocketListenerConnectionReceivedEventArgs args)
        {
            try
            {
                // Stop advertising/listening so that we're only serving one client
                _provider.StopAdvertising();
                listener.Dispose();
                _socket = args.Socket;
                Debug.WriteLine("Successfully stoped listening to the sock.");
            }
            catch (Exception ex)
            {
                Debug.WriteLine("Error on server start." + ex.ToString());
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
                        .WithRetainFlag()
                        .Build();
            await _mqttClient.PublishAsync(message);
            Debug.WriteLine("Successfuly published the message.");
        }

        private async void ConnectClient(object sender, RoutedEventArgs e)
        {
            if (!_mqttClient.IsConnected)
            {
                try
                {
                    await _mqttClient.ConnectAsync(_clientOptionBuilder.Build());
                    Debug.WriteLine("Client is trying to connect to the mqtt server.");
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

        private async void DisconnectClient(object sender, RoutedEventArgs e)
        {
            if (_mqttClient.IsConnected)
            {
                try
                {
                    await _mqttClient.DisconnectAsync();
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