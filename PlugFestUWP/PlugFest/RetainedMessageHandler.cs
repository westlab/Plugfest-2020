using MQTTnet;
using MQTTnet.Server;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PlugFest
{
    class RetainedMessageHandler : IMqttServerStorage
    {
        // private const string Filename = "retainStorage.json";
        public string TEDSStringA { get; set; }
        public string TEDSStringB { get; set; }
        public string TEDSStringC { get; set; }
        // private Windows.Storage.StorageFolder storageFolder;
        // private Windows.Storage.StorageFile retainFile;
        private IList<MqttApplicationMessage> retainList = new List<MqttApplicationMessage>();
        // private String[] topicList = {"PlugFest/sensors/A/integrated", "PlugFest/sensors/B/integrated", "PlugFest/sensors/C/integrated", "PlugFest/sensors/A/TEDS", "PlugFest/sensors/B/TEDS", "PlugFest/sensors/C/TEDS"};
        private Hashtable topicMsgConnector = new Hashtable();
        private void InitTEDS()
        {
            MqttApplicationMessage TEDSA = new MqttApplicationMessage();
            MqttApplicationMessage TEDSB = new MqttApplicationMessage();
            MqttApplicationMessage TEDSC = new MqttApplicationMessage();
            MqttApplicationMessage TEDSSepA = new MqttApplicationMessage();
            MqttApplicationMessage TEDSSepB = new MqttApplicationMessage();
            MqttApplicationMessage TEDSSepC = new MqttApplicationMessage();
            TEDSA.Payload = System.Text.Encoding.Unicode.GetBytes(TEDSStringA);
            TEDSA.Retain = true;
            TEDSA.Topic = "PlugFest/sensors/A/integrated";
            TEDSB.Payload = System.Text.Encoding.Unicode.GetBytes(TEDSStringB);
            TEDSB.Retain = true;
            TEDSB.Topic = "PlugFest/sensors/B/integrated";
            TEDSC.Payload = System.Text.Encoding.Unicode.GetBytes(TEDSStringC);
            TEDSC.Retain = true;
            TEDSC.Topic = "PlugFest/sensors/C/integrated";

            TEDSSepA.Payload = System.Text.Encoding.Unicode.GetBytes(TEDSStringA);
            TEDSSepA.Retain = true;
            TEDSSepA.Topic = "PlugFest/sensors/A/TEDS";
            TEDSSepB.Payload = System.Text.Encoding.Unicode.GetBytes(TEDSStringB);
            TEDSSepB.Retain = true;
            TEDSSepB.Topic = "PlugFest/sensors/B/TEDS";
            TEDSSepC.Payload = System.Text.Encoding.Unicode.GetBytes(TEDSStringC);
            TEDSSepC.Retain = true;
            TEDSSepC.Topic = "PlugFest/sensors/C/TEDS";

            retainList.Add(TEDSA);
            retainList.Add(TEDSB);
            retainList.Add(TEDSC);
            retainList.Add(TEDSSepA);
            retainList.Add(TEDSSepB);
            retainList.Add(TEDSSepC);
        }

        private void UpdateTEDS()
        {
            topicMsgConnector["PlugFest/sensors/A/integrated"] = TEDSStringA;
            topicMsgConnector["PlugFest/sensors/B/integrated"] = TEDSStringB;
            topicMsgConnector["PlugFest/sensors/C/integrated"] = TEDSStringC;
            topicMsgConnector["PlugFest/sensors/A/TEDS"] = TEDSStringA;
            topicMsgConnector["PlugFest/sensors/B/TEDS"] = TEDSStringB;
            topicMsgConnector["PlugFest/sensors/C/TEDS"] = TEDSStringC;

            foreach (String topicName in topicMsgConnector.Keys)
            {
                try
                {
                    retainList.Where(elem => elem.Topic == topicName).First().Payload = System.Text.Encoding.Unicode.GetBytes((String)topicMsgConnector[topicName]);
                }
                catch (Exception)
                {
                    Debug.WriteLine("Went wrong");
                    throw;
                }
            }
        }

        public RetainedMessageHandler()
        {
            TEDSStringA = "6A4000200401000064000000100000308C04000000008E3EBFCBE8FA390C00";
            TEDSStringB = "7A4000200401000064000000100000308C04000000008E3EBFCBE8FA390C00";
            TEDSStringC = "8A4000200401000064000000100000308C04000000008E3EBFCBE8FA390C00";
            InitTEDS();
        }

        public Task SaveRetainedMessagesAsync(IList<MqttApplicationMessage> messages)
        {
            // There should be better implementation....
            // File.WriteAllText(Filename, JsonConvert.SerializeObject(messages));
            foreach (MqttApplicationMessage message in messages)
            {
                bool alreadyExist = false;
                for (int i = 0; i < retainList.Count; i++)
                {
                    if (message.Topic == retainList[i].Topic)
                    {
                        retainList[i] = message;
                        alreadyExist = true;
                    }
                }
                if (!alreadyExist)
                {
                    retainList.Add(message);
                }
            }
            UpdateTEDS();
            Debug.WriteLine("Retain message");
            return Task.FromResult(0);
        }

        public Task<IList<MqttApplicationMessage>> LoadRetainedMessagesAsync()
        {
            return Task.FromResult(retainList);
        }
    }
}
