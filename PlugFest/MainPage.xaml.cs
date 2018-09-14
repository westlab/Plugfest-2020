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
using MQTTnet.Adapter;
using MQTTnet.Diagnostics;
using MQTTnet.Protocol;
using System.Diagnostics;
using System.Text;

// 空白ページの項目テンプレートについては、https://go.microsoft.com/fwlink/?LinkId=402352&clcid=0x411 を参照してください

namespace PlugFest
{
    /// <summary>
    /// それ自体で使用できる空白ページまたはフレーム内に移動できる空白ページ。
    /// </summary>
    public sealed partial class MainPage : Page
    {
        private IMqttServer mqttServer = new MqttFactory().CreateMqttServer();
        private bool isServerRunning = false;
        public bool IsServerRunning { get => isServerRunning; set => isServerRunning = value; }
        private System.Net.IPAddress bindAddr;
        private MqttServerOptionsBuilder optionBuilder;
        RfcommServiceProvider _provider;
        StreamSocket _socket;

        public MainPage()
        {
            this.InitializeComponent();
            // UWP won't allow you to bind loopback addr.
            // bindAddr = System.Net.IPAddress.Parse("127.0.0.1");
            // bindAddr = System.Net.IPAddress.Parse("192.168.56.1");
            optionBuilder = new MqttServerOptionsBuilder()
                .WithConnectionBacklog(100)
                //.WithDefaultEndpointBoundIPAddress(bindAddr)
                .WithDefaultEndpointPort(1883);

        }


        private async void StartServer(object sender, RoutedEventArgs e)
        {
            if (!IsServerRunning)
            {
                try
                {
                    IsServerRunning = true;
                    mqttServer = new MqttFactory().CreateMqttServer();
                    mqttServer.ApplicationMessageReceived += MqttServer_ApplicationMessageReceived;
                    mqttServer.ClientConnected += MqttServer_ClientConnected;
                    mqttServer.ClientDisconnected += MqttServer_ClientDisconnected;
                    await mqttServer.StartAsync(optionBuilder.Build());
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
                    await mqttServer.StopAsync();
                    IsServerRunning = false;
                    Debug.WriteLine("Server stoped.");
                }
                catch (Exception ex)
                {
                    Debug.WriteLine("Error on server hutdown." + ex.ToString());
                    throw;
                }

            }
        }
        
        private static void MqttServer_ClientConnected(object sender, MqttClientConnectedEventArgs e)
        {
            Debug.WriteLine($"Client[{e.ClientId}] connected");
        }

        private static void MqttServer_ClientDisconnected(object sender, MqttClientDisconnectedEventArgs e)
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
            StreamSocketListener listener = new StreamSocketListener();
            listener.ConnectionReceived += OnConnectionReceived;
            await listener.BindServiceNameAsync(_provider.ServiceId.AsString(), SocketProtectionLevel.BluetoothEncryptionAllowNullAuthentication);

            // Set the SDP attributes and start advertising
            InitializeServiceSdpAttributes(_provider);
            _provider.StartAdvertising(listener);
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

        private void OnConnectionReceived(StreamSocketListener listener, StreamSocketListenerConnectionReceivedEventArgs args)
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
        }

    }
}