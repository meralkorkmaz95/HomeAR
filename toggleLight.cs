using Vuforia;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public class toggleLight : MonoBehaviour, ITrackableEventHandler {
	
	private TrackableBehaviour mTrackableBehaviour;
	
	private bool mShowGUIButton = false;
	private Rect mButtonRect = new Rect(50,50,120,60);
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
            mShowGUIButton = true;
        }
        else
        {
            mShowGUIButton = false;
        }
    }
	
	void OnGUI() {
		if (mShowGUIButton) {
			if(GUI.Button(new Rect(10, 50, 100, 20), "ON"))
            {
                int res = Upload("ON"); 
            }
            if(GUI.Button(new Rect(10, 90, 100, 20), "OFF"))
            {
                int res = Upload("OFF"); 
            }
		}
	}

    int Upload(string status) {
        WWWForm form = new WWWForm();
        form.AddField("Status", status);
 
        UnityWebRequest req = UnityWebRequest.Post(Server_Address+"/toggleLight", form);
        req.SendWebRequest();
 
       while (!req.isDone) 
        {
        }

        if (req.isNetworkError)
        {
            Debug.Log("Server Connection Error: " + req.error);
            return 0;
        }  
        else{
            return 1; 
        }
    }
}
