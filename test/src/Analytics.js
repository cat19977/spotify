import React from "react";
import "./Analytics.css";
import * as $ from "jquery";

class Analytics extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            genres: ''
        };
        this.token = ''
        this.genres = ''
        this.get_token = this.get_token.bind(this);
        this.get_genres = this.get_genres.bind(this);
    }
    componentWillMount(){
        this.get_token()
    }
    
    componentDidMount(){
        this.getData()
    }
    get_token(){
        $.ajax({
            url: `http://127.0.0.1:5000/add_token`,
            type: "GET",
            success: (data) => {
                this.token = data;
            }
          });
    }
    
    getData(){
        setTimeout(() => {
          this.get_genres()
        }, 1000)
      }
    
      get_genres(){
        const uris = this.props.artist_data;
        const header = JSON.parse(this.token['header']);
        const genres = []
        for(let uri in uris){
            $.ajax({
                url: `${uris[uri]}`,
                type: "GET",
                headers: {
                    'Authorization': header['Authorization']
                },
                success: (data) => {
                    const genre = data['genres']
                    genres.push(genre)
                }
              });
        }
        this.genres = genres
    }

    render() {
        console.log(this.genres)
        return (
            <div className='data'>Hey</div>

        );
    }




}
export default Analytics;