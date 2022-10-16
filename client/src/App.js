import React, { useState, useEffect } from 'react'
import './App.css';

function App() {

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

  this.uploadFile = async(e) => {
    const message_folder = e.target.files;
    if (message_folder != null) {
      const data = new FormData();
      data.append('message_folder', message_folder);

      let response = await fetch('/upload',
      {
        method: 'post',
        body: data,
      });
      let result = await response.json();
      if (result.status !== 1) {
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
          <input type="file" webkitdirectory="" mozdirectory="" directory="" onChange={this.uploadFile} />
      </label>
    </div>
  );
}

export default App;
