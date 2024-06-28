import React, { useEffect, useState } from "react";
import botImage from "../assets/images/bit_image.jpeg" 
import {
  MDBContainer,
  MDBRow,   
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBIcon,
  MDBTypography,
  MDBInput,  
} from "mdb-react-ui-kit";
import "./Chatroom.css"
import Scrollbars from "react-custom-scrollbars-2"

export default function Chatroom() {
    const [selectedFiles,setSelectedFiles] = useState([])
    const [chatHistory, setChatHistory] = useState([])
    const [chatMessages,setChatMessages] = useState([])

    const fetchUserChats= ()=> {
      fetch("http://127.0.0.1:8000/doc_query/chat/",{
        method : "GET",
        headers: {
          "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3QyQGdtYWlsLmNvbSIsImV4cCI6MTcxOTkyMjQ5M30.bl6vShNqutBa2bQG9QmN895iiQLN5QgJFB7Z2XaLRFM",
          "Content-Type" : "application/json"
        }
      })
      .then((response)=>{
        if(!response.ok){
          throw new Error("Server response was not ok")
        }
        return response.json()
      })
      .then((data)=>{
        console.log(data)
        setChatHistory(data)})
      .catch((error) =>console.error("There was a problem with the fetch operation:", error))
    }
    useEffect(()=>{
      console.log("Fetching User Chats...")
      fetchUserChats()
    },[])

    const createNewChat = ()=>{
      console.log("Creating New Chat......")
      const chat_title = window.prompt("Enter Chat Title:","MyChat");
      if (chat_title!== null && chat_title.length>0 ){
        fetch("http://127.0.0.1:8000/doc_query/chat/",{
          method: "POST",
          headers: {
            "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3QyQGdtYWlsLmNvbSIsImV4cCI6MTcxOTkyMjQ5M30.bl6vShNqutBa2bQG9QmN895iiQLN5QgJFB7Z2XaLRFM",
            "Content-Type" : "application/json"
          },
          body:JSON.stringify({
            title : `${chat_title}`,
            owner_id : '667d57bdd13419882b162742'
          })
        }).then((response)=>{
          if(!response.ok){
            console.log("error")
            throw new Error("Server response was not ok")
          }
          return response.json()
        })
        .then((data)=>{
          console.log(data)
          console.log("fethcing here")
          fetchUserChats()
          console.log(chatHistory[0].id)
          console.log(chatHistory[0].title)
          fetchChatMessages(chatHistory[0].id)
        })
        .catch((error) => console.error('There was a problem with the fetch operation:', error));
  }
  else{
    console.log("In else doing nothing")
  }
     };


    const uploadFiles = ()=>{
      console.log("Uploading Files")
    }


    const handleFileChange =(event)=>{
      const files = Array.from(event.target.files)
      setSelectedFiles(files)
    }

    const fetchChatMessages = (chatid) =>{
      console.log("Fetching Chat Messages....", chatid)
      fetch(`http://127.0.0.1:8000/doc_query/chat/${chatid}/messages`,{
        method:"GET",
        headers: {
          "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3QyQGdtYWlsLmNvbSIsImV4cCI6MTcxOTkyMjQ5M30.bl6vShNqutBa2bQG9QmN895iiQLN5QgJFB7Z2XaLRFM",
          "Content-Type" : "application/json"
        }
      }
      )
      .then((response)=>{
        if(!response.ok){
          console.log("error")
          throw new Error("Server Response was not ok")
        }
        return response.json()
      })
      .then((data)=>{
        console.log(data)
        setChatMessages(data)
      })
      .catch((error)=> console.error('There was a problem with the fetch operation:', error))
    }

    const formatDate = (utcdate) => {
      const new_date = new Date(utcdate + 'Z')
      const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      };
      return new_date.toLocaleString('en-US', options)
    };

  return (
    <MDBContainer fluid className="py-5" style={{ backgroundColor: "#CDC4F9" }}>
      <MDBRow>
        <MDBCol md="12">
          <MDBCard id="chat3" style={{ borderRadius: "15px" }}>
            <MDBCardBody>
              <MDBRow>
                {/* CHAT HISTORY SECTION */}
                <MDBCol md="6" lg="5" xl="4" className="mb-4 mb-md-0">
                  <div className="p-3">
                    <div style={{display: "flex" , justifyContent: "space-evenly"}}>
                      <h3>Chat History</h3>
                      <button style={{border: "none", borderRadius: "5px", background: "blue", width : "125px" , color: "white"}}
                      onMouseOver={(e)=>e.target.style.background = "#0f0352"} onMouseOut={(e)=> e.target.style.background="blue"} onClick={createNewChat}>New Chat</button>
                    </div>
                    <Scrollbars
                      style={{ position: "relative", height: "400px" }}
                    >
                      <MDBTypography listUnStyled className="mb-0">
                        {chatHistory.length > 0 &&
                        chatHistory.map((chat)=>{
                          return <li key= {chat.id} className="p-2 border-bottom" onClick={()=>fetchChatMessages(chat.id)}>
                          <a
                            href="#!"
                            className="d-flex justify-content-between"
                          >
                            <div className="d-flex flex-row">
                              <div className="pt-1">
                                <p className="fw-bold mb-0">{chat.title}</p>
                              </div>
                            </div>
                            <div className="pt-1">
                              <p className="small text-muted mb-1">{formatDate(chat.creation_timestamp)}</p>   
                            </div>
                          </a>
                        </li>
                        })
                        }
                      </MDBTypography>
                    </Scrollbars>
                  </div>
                </MDBCol>
                <MDBCol md="6" lg="5" xl="4" style={{marginTop:"20px"}}>
                    <h3>Upload PDFs</h3>
                        <Scrollbars 
                            style={{position:"relative" , height: "400px"}}
                            >
                                {selectedFiles.length > 0 && (
                                    <div className="mt-3">
                                        <h5>Selected Files:</h5>
                                        <ul>
                                            {selectedFiles.map((item,index) => {
                                                return (
                                                    <li key={index}>{item.name}</li>
                                                )
                                            })}
                                        </ul>
                                    </div>
                                )}
                        </Scrollbars>
                        <div className="justify-content-start align-items-center" style={{color:"green"}}>   
                        <form onSubmit={uploadFiles}>
                            <div style={{display:"flex"}}>
                                <MDBInput
                                onChange={handleFileChange}
                                type="file"
                                accept=".pdf"
                                required
                                multiple
                                >
                                </MDBInput>
                                <button type="submit" style={{borderRadius:"5px",background : "blue" , color: "white", border:"none", width: "125px"}} onMouseOver={(e)=>e.target.style.background = "#0f0352"} onMouseOut={(e)=> e.target.style.background="blue"}>Upload</button>
                            </div>
                        </form>
                        </div>
                </MDBCol>
                <MDBCol md="6" lg="5" xl="4">
                  <Scrollbars
                    style={{ position: "relative", height: "400px" }}
                    className="pt-3 pe-3"
                  >
                    {/* DISPLAY CHAT MESSAGES */}
                    {chatMessages.length === 0 && (
                      <div className="d-flex justify-content-center align-items-center" style={{height:"100%"}}>
                        <h4 className="large rounded-3 text-muted" style={{background: "lightblue", width:"250px", paddingLeft: "15px"}}>No messages so far!</h4>
                      </div>
                    )}
                    {chatMessages.length>0 && (
                      chatMessages.map((msg)=>{
                        if (msg.type === "MessageType.USER"){
                          return <div key={msg.id} className="d-flex flex-row justify-content-start">
                                                  <img
                        src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava6-bg.webp"
                        alt="avatar 1"
                        style={{ width: "45px", height: "100%" }}
                      />
                          <div>
                            <p
                              className="small p-2 ms-3 mb-1 rounded-3"
                              style={{ backgroundColor: "#f5f6f7" }}
                            >
                              {msg.msg_txt}
                            </p>
                            <p className="small ms-3 mb-3 rounded-3 text-muted float-end">
                              {formatDate(msg.creation_timestamp).split(",")[2]}
                            </p>
                          </div>
                        </div>
                        }
                        else{
                          return <div key={msg.id} className="d-flex flex-row justify-content-end">
                          <div>
                            <p className="small p-2 me-3 mb-1 text-white rounded-3 bg-primary">
                              {msg.msg_txt}
                            </p>
                            <p className="small me-3 mb-3 rounded-3 text-muted">
                              {formatDate(msg.creation_timestamp).split(",")[2]}
                            </p>
                          </div>
                          <img
                            src={botImage}
                            alt="BOT"
                            style={{ width: "45px", height: "100%" }}
                          />
                        </div>
                        }
                      })
                    )}
                  </Scrollbars>
                  <div className="text-muted d-flex justify-content-start align-items-center pe-3 pt-3 mt-2">
                    <img
                      src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava6-bg.webp"
                      alt="avatar 3"
                      style={{ width: "40px", height: "100%" }}
                    />
                    <input
                      type="text"
                      className="form-control form-control-lg"
                      id="exampleFormControlInput2"
                      placeholder="Type message"
                    />
                    <a className="ms-1 text-muted" href="#!">
                      <MDBIcon fas icon="paperclip" />
                    </a>
                    <a className="ms-3 text-muted" href="#!">
                      <MDBIcon fas icon="smile" />
                    </a>
                    <a className="ms-3" href="#!">
                      <MDBIcon fas icon="paper-plane" />
                    </a>
                  </div>
                </MDBCol>
              </MDBRow>
            </MDBCardBody>
          </MDBCard>
        </MDBCol>
      </MDBRow>
    </MDBContainer>
  );
}