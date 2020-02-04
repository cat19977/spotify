import React, { Component } from "react";
import {Router} from "@reach/router";
import Top from "./Top";
import Home from "./Home";
import Login from "./Login";


class Route extends Component{
    render(){
        return(
            <Router>
                <Login path="/"/>
                <Home path="/home" />
                <Top path="/top"/>
            </Router>
            
        );
    }

}

export default Route;