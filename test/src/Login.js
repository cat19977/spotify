import React, { Component } from "react";
import { authEndpoint, clientId, redirectUri, scopes } from "./config";
import hash from "./hash";
import "./Login.css";
import Home from "./Home"
import * as $ from "jquery";

class Login extends Component {
  constructor() {
    super();
    this.state = {
      token: null,
      hasToken: false,
      loading: true
    };
    this.componentDidMount = this.componentDidMount.bind(this);
  }
  
  
  componentDidMount() {
    // Set token
    let _token = hash.access_token;
    if (_token) {
      // Set token
      this.setState({
        token: _token,
        hasToken: true,
        loading: false
      });
      window.token = _token;
    $.ajax({ 
      url: 'http://127.0.0.1:5000/add_token', 
      type: 'POST', 
      crossDomain: true,
      data: JSON.stringify({'token':_token}),
      dataType: 'json',
      success: function(response){ 
          $('#main').text(response)
          this.setState({
            loading: false
          }); 
        } 
      });
      }
    }
  
    renderLoading() {
      return <div>Loading...</div>;
    }
  

  render(){

    return (
      <body className='login'>
        <div className="login-header">
          {!this.state.token && (
            <a
              className="btn btn--loginApp-link"
              href={`${authEndpoint}?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes.join(
                "%20"
              )}&response_type=token&show_dialog=true`}
            >
              Login to Spotify
            </a>
          )}
          {this.state.token && (
            <Home />
          )}
          </div>
      </body>
    );
  }
  }

  
  export default Login;
  
  