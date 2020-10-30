import React, { Component }from "react";
import "./App.css";
import Route from "./Route";
import * as $ from "jquery";
import Home from "./Home"


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      haveToken: false
    };
    this.haveToken = this.haveToken.bind(this);
  }

  componentDidMount() {
    this.haveToken()
  }

  //gets top tracks based on time (short,med,long term)
  haveToken() {
    // Make a call using the token
    $.ajax({
      url: `http://127.0.0.1:5000/add_token`,
      type: "GET",
      success: (data) => {
        if (data['token'] === 'true') {
          this.setState({
            haveToken: true
          })
        }
      }
    });
  }


  render() {
    return (
      <div className='App'>
        {this.state.haveToken ?
            <Home /> :
            <Route />
        }
      </div>
    );
  }
}
  
  
  export default App;
