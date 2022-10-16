import React, { useState, useEffect } from 'react'
import './App.css';

function App() {
    const [emojiUsage, setEmojiUsage] = useState();

    const handleEmojiUsageClick = (e) => {
        fetch("/emoji_usage").then((response) => {
            if (response.status == 200) {
                return response.json();
               // console.log(response.json());
            }
        }).then(setEmojiUsage)
        a();
    }

    function a() {
        console.log("Harmony")
    }


  /*const [data, setData] = useState([{}])
  useEffect(() => {
    fetch("/members").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, []) 
  
        {(typeof data.members === 'undefined') ? (
        <p> Loading... </p>
      ) :  (
        data.members.map((member, i) => (
          <p key={i}>{member}</p>
        ))
      )}*/

      /*
      async function uploadFile(e) {
      */

  //this.uploadFile = async(e) => {
    async function uploadFile(e) {
    const message_folder = e.target.files;
    if (message_folder != null) {
      const data = new FormData();
      data.append('message_folder', message_folder);

      /*let response = await fetch('/upload',
      {
        method: 'post',
        body: data,
      });
      let result = await response.json();
      if (result.status !== 1) {
        alert('Error uploading file')
      }*/

      const response = await fetch("/upload", 
      {
        // Data will be serialized and sent as json
        method: "POST",
        body: data,
            
        // stuff we want to send
        // tell the server we're sending JSON
        headers: {
            "Content-Type": "application/json"
        },
      });
      if (!response.ok) {
        alert('Error uploading file')
      }
    }
  }

  return (
    <div>
      <div style={{ width: '100%', float: 'left' }}>
        <h3>Click the button to upload your data</h3> <br />
      </div>
      <label htmlFor="contained-button-file">
          <input type="file" webkitdirectory="" mozdirectory="" directory="" onChange={uploadFile} />
      </label>

      <button onClick={handleEmojiUsageClick}> Emojiii </button>
      <p>
          {
          JSON.stringify(emojiUsage)
//          Object.keys(emojiUsage).map((key, index) => (
//            <p key={index}> this is my key {key} and this is my value {emojiUsage[key]}</p>
//          ))
        }
      </p>
    </div>


  );
}
export default App;
