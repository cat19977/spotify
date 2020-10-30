import React from "react";
import "./Analytics.css";
import * as $ from "jquery";
import '@trendmicro/react-sidenav/dist/react-sidenav.css';
import SideBar from "./SideBar";
import Graph from "./Graph";

class Analytics extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            genres: [],
            artists: [],
            data_type: 'genres/piechart'
        };
        this.get_artists = this.get_artists.bind(this);
        this.get_genres = this.get_genres.bind(this);
    }
    
    componentDidMount(){
        this.get_genres()
        this.get_artists();
    }
    
    get_genres() {
        const term = this.props.term;
        $.ajax({
            url: `http://127.0.0.1:5000/get-genres?term=${term}`,
            type: "GET",
            success: (data) => {
                console.log(data)
                this.setState({
                    loading: false,
                    genres: data,
                })
            }
        });
    }

    get_artists() {
        const term = this.props.term;
        $.ajax({
            url: `http://127.0.0.1:5000/get-artists?term=${term}`,
            type: "GET",
            success: (data) => {
                console.log(data)
                this.setState({
                    loading: false,
                    artists: data,
                })
            }
        });
    }

    myCallback = (dataFromChild) => {
        this.setState({
            data_type: dataFromChild
        })
    }

    render() { 
        if(this.state.loading){
            return <div>Loading</div>
        }
        else{
        return (
            <div className='Analytics'>
                <div>
                    <div><SideBar data_type={this.myCallback}/></div>
                    <Graph data_type={this.state.data_type} genres={this.state.genres} artists={this.state.artists}/>
                </div>
                
            </div>
        )
        }
    }
}

export default Analytics;