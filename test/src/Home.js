import React, { Component } from "react";
import './Home.css';
import Top from './Top'
import * as $ from "jquery";


class Home extends Component {
  //todo: get data from db here and then pass it to components based on state
  constructor(props) {
    super(props);
    this.state = {
      show_term: '',
      top_short: '',
      top_med: '',
      top_long: '',
      saved_data: '',
      recent_data: '',
      loading: false
    };
    this.getData = this.getData.bind(this);
  }

  componentDidMount() {
    this.getData()
  }


  getData() {
    var root = 'http://127.0.0.1:5000/get-songs?'
    var p = [];

    p.push($.ajax({ url: root + 'term=short_term', type: "GET" }));
    p.push($.ajax({ url: root + 'term=medium_term', type: "GET" }));
    p.push($.ajax({ url: root + 'term=long_term', type: "GET" }));
    p.push($.ajax({ url: root + 'term=saved', type: "GET" }));
    p.push($.ajax({ url: root + 'term=recent', type: "GET" }));

    Promise.all(p).then(values => {
      this.setState({
        top_short: values[0],
        top_med: values[1],
        top_long: values[2],
        saved_data: values[3],
        recent_data: values[4],
        loading: false
      });
    });
  }

  onTopClick(time) {
    this.setState({
      show_term: time,
    });
  }

  renderLoading() {
    return <div>Loading...</div>;

  }

  renderPosts() {
    const term = this.state.show_term;
    let top;

    if (term === 'saved') {
      top = <Top data={this.state.saved_data} time={this.state.show_term} />;
    } else if (term === 'short_term') {
      top = <Top data={this.state.top_short} time={this.state.show_term} />;
    } else if (term === 'medium_term') {
      top = <Top data={this.state.top_med} time={this.state.show_term} />;
    } else if (term === 'long_term') {
      top = <Top data={this.state.top_long} time={this.state.show_term} />;
    } else {
      top = <Top data={this.state.recent_data} time={this.state.show_term} />;
    }
    return (
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
          <button className="dropbtn1" onClick={() => this.onTopClick('recent')}>Recently Played</button>
        </div>
        {top}
      </div>
    );
  }



  render() {
    return (
        this.state.loading ?
          this.renderLoading()
          : this.renderPosts()
      )

  }
}

export default Home;
