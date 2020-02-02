import React, { Component }from "react";
import {useEffect} from "react";
import "./App.css";
import Route from "./Route";
import MyComponent from "./api"
import * as $ from "jquery";


class App extends Component {
  constructor(props){
    super(props);
    this.state = {
      token:''
    };
  }

  render() {
    return (
      <div className='App'>
        <Route />
      </div>
    );
  }
}
  
  
  export default App;
