using Vuforia;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public class avgTemp : MonoBehaviour, ITrackableEventHandler {
    public double [] temp = new double[5];
    public double [] time = new double[5];

    [Serializable]
    public class avgTempObject
    {
        public double avgTime;
        public double avgTemp;
    }

    public static class JsonHelper
    {
        public static T[] FromJson<T>(string json)
        {
            Wrapper<T> wrapper = JsonUtility.FromJson<Wrapper<T>>(json);
            return wrapper.avgTempData;
        }

        [Serializable]
        private class Wrapper<T>
        {
            public T[] avgTempData;
        }
    }
    
    private TrackableBehaviour mTrackableBehaviour;
    
    private bool mShowGUILabel = false;
    private Rect mLabelRect = new Rect(50,50,120,60);
	private string Server_Address = "http://meralkorkmaz95.pythonanywhere.com";

    void Start () {
        mTrackableBehaviour = GetComponent<TrackableBehaviour>();
        if (mTrackableBehaviour)
        {
            mTrackableBehaviour.RegisterTrackableEventHandler(this);
        }
    }
    
    public void OnTrackableStateChanged(
                                    TrackableBehaviour.Status previousStatus,
                                    TrackableBehaviour.Status newStatus)
    {
        if (newStatus == TrackableBehaviour.Status.DETECTED ||
            newStatus == TrackableBehaviour.Status.TRACKED)
        {
            mShowGUILabel = true;
        }
        else
        {
            mShowGUILabel = false;
        }
    }
    
    void OnGUI() {
        if (mShowGUILabel) {
            var avgTempData = getAvgTempData();

            int i = 0; 
            foreach (var data in avgTempData)
            {
                temp[i] = data.avgTemp; 
                time[i] = data.avgTime;
                i = i + 1;  
            }
            //Here we have to draw the graph! 
            GUI.Label(new Rect(10, 10, 1000, 200), "Current Average Temperature: " + temp[3].ToString());
        }
    }

    public IEnumerable<avgTempObject> getAvgTempData()
    {
        UnityWebRequest req = UnityWebRequest.Get(Server_Address + "/getAvgTemp");
        req.SendWebRequest();

        while (!req.isDone)
        {
        }

        if (req.isNetworkError)
        {
            Debug.Log("Server Connection Error: " + req.error);

            return null;
        }
        else
        {
            string response = req.downloadHandler.text;
            Debug.Log(response); 
            avgTempObject[] avgTempData = JsonHelper.FromJson<avgTempObject>(response);

            return avgTempData;
        }
    }


}
