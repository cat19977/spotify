import React, { Component } from "react";
import './Home.css';
import Top from './Top'
import * as $ from "jquery";

class Home extends Component{
   //todo: get data from db here and then pass it to components based on state
    constructor(props){
        super(props);
        this.state = {
            show_term: ''
        };
      this.top_data = '';
      this.getTopTracks = this.getTopTracks.bind(this);
      this.onTopClick = this.onTopClick.bind(this);
    }

    componentDidMount(){
      this.getTopTracks()
    }
  
       //gets top tracks based on time (short,med,long term)
     getTopTracks(time) {
    // Make a call using the token
    $.ajax({
      url: `http://127.0.0.1:5000/get-top-songs`,
      type: "GET",
      success: (data) => {
          this.top_data = data
      }
    });
    }
  
  onTopClick(time) {
    this.setState({
      show_term: time,
    });
  }
  
    render(){
        return(
            <div className='back'>
              <div className="navbar">
                <div className='dropdown'>
                  <button className="dropbtn">Top Songs
                    <i className="fa fa-caret-down"></i>
                  </button>
                  <div className="dropdown-content">
                      <button onClick={() => this.onTopClick('short_term')}>Short-Term</button>
                      <button onClick={() => this.onTopClick('medium_term')}>Medium-Term</button>
                      <button onClick={() => this.onTopClick('long_term')}>Long-Term</button>
                  </div>
                </div>
              </div>
              {this.state.show_term ?
                  <Top data={this.top_data} time={this.state.show_term} /> :
                   null
              }
            </div>
        );
    }
}

export default Home;
