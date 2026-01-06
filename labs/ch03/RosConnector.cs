using UnityEngine;
using RosSharp.RosBridgeClient;
using RosMessageTypes.Sensor;

public class RosConnector : MonoBehaviour
{
    public string jointStatesTopic = "/joint_states";
    public GameObject robot; // Assign your robot model in the Unity Editor

    private RosSocket rosSocket;
    private ArticulationBody[] jointArticulationBodies;

    void Start()
    {
        // Get all ArticulationBody components in the robot model
        jointArticulationBodies = robot.GetComponentsInChildren<ArticulationBody>();

        // Start the ROS connection
        rosSocket = new RosSocket(new RosBridgeClient.Protocols.WebSocketProtocol("ws://localhost:9090"));
        rosSocket.Subscribe<JointState>(jointStatesTopic, JointStateCallback);
    }

    void JointStateCallback(JointState msg)
    {
        for (int i = 0; i < msg.name.Length; i++)
        {
            string jointName = msg.name[i];
            float jointPosition = (float)msg.position[i];

            foreach (var joint in jointArticulationBodies)
            {
                if (joint.name == jointName)
                {
                    var drive = joint.xDrive;
                    drive.target = Mathf.Rad2Deg * jointPosition;
                    joint.xDrive = drive;
                    break;
                }
            }
        }
    }

    void OnDestroy()
    {
        if (rosSocket != null)
        {
            rosSocket.Close();
        }
    }
}
