import React, { Component } from "react";
import './Home.css';
import Top from './Top'
import * as $ from "jquery";

class Home extends Component{
   //todo: get data from db here and then pass it to components based on state
    constructor(props){
        super(props);
        this.state = {
            show_term: '',
        };
      this.top_data = '';
      this.saved_data = '';
      this.getTopTracks = this.getTopTracks.bind(this);
      this.getSavedTracks = this.getSavedTracks.bind(this);
      this.onTopClick = this.onTopClick.bind(this);
    }

    componentDidMount(){
      this.getTopTracks()
      this.getSavedTracks()
    }
  
       //gets top tracks based on time (short,med,long term)
     getTopTracks() {
    // Make a call using the token
    $.ajax({
      url: `http://127.0.0.1:5000/get-top-songs`,
      type: "GET",
      success: (data) => {
          this.top_data = data
      }
    });
    }

    getSavedTracks() {
      // Make a call using the token
      $.ajax({
        url: `http://127.0.0.1:5000/get-saved-songs`,
        type: "GET",
        success: (data) => {
            this.saved_data = data
        }
      });
      }
  
  onTopClick(time) {
    this.setState({
      show_term: time
    });
  }

    render(){
      const term = this.state.show_term;
      let top;
      
      if (term === 'saved') {
          top = <Top data={this.saved_data} time={this.state.show_term} />;
      } else {
          top = <Top data={this.top_data} time={this.state.show_term} /> ;
      }
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
                <button className="dropbtn1" onClick={() => this.onTopClick('saved')}>Saved Songs </button>
              </div>
              {top}
            </div>
        );
    }
}

export default Home;
