import React from "react";
import "./Analytics.css";
import Plot from 'react-plotly.js';
import '@trendmicro/react-sidenav/dist/react-sidenav.css';


class Graph extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            type: 'pie',
        }
        this.data_genres = '';
        this.data_artisis = '';
        this.get_data_genres = this.get_data_genres.bind(this);
        this.get_data_artists =  this.get_data_artists.bind(this);
    }

    get_data_genres(){
        var genres = this.props.genres['data'].slice(0, 11);
        var names = []
        var counts = []
        for (var genre in genres) {
            genre = genres[genre]
            names.push(genre['name'])
            counts.push(genre['count'])
        }
        
        var type = this.props.data_type.split("/")[1].split("c")[0];
        var data;
        if(type === 'bar'){
            data=[
                {
                    type: type,
                    y: names.reverse(),
                    x: counts.reverse(),
                    orientation: 'h'
                }
            ]
        }
        else{
            data=[
                {
                    type: type,
                    labels: names.reverse(),
                    values: counts.reverse(),
                }
            ]
        }
        this.data_genres = data;
    }

    get_data_artists(){
        var artists = this.props.artists['data'];
        var names = []
        var counts = []
        for (var artist in artists) {
            artist = artists[artist]
            names.push(artist['name'])
            counts.push(artist['count'])
        }
        var values = [
            names,
            counts]
      
      var data = [{
        type: 'table',
        header: {
          values: [["<b>Artist</b>"], ["<b>Count</b>"]],
          align: ["center", "center"],
          line: {width: 1, color: '#1ecd97'},
          fill: {color: '#1ecd97'},
          font: {family: "Arial", size: 15, color: "white"}
        },
        cells: {
          values: values,
          align: ["left", "center"],
          height: 30,
          line: {color: "#1ecd97", width: 1},
           fill: {color: ['rgba(0,0,0,0)', 'rgba(0,0,0,0)']},
          font: {family: "Arial", size: 15, color: ["white"]}
        }
      }]
      this.data_artists = data;
    }

    render(){
        var data;
        var title;
        if(this.props.data_type.includes("genres")){
            this.get_data_genres();
            data = this.data_genres;
            title = "Top Genres"
        }
        if(this.props.data_type.includes("artists")){
            this.get_data_artists();
            data = this.data_artists;
            console.log(this.data_artists);
            title = "Top Artists"
        }
        const layout= ({ width: 700, 
            height: 500, 
            title: title,
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font:{color: 'white'} })
        
        return(
            <Plot
            data={data}
            layout={layout}
            />)
        }
}
export default Graph;

