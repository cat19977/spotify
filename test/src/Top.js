import React from "react";
import "./top.css";
import Analytics from "./Analytics";

function Table(props) {
  var listData = props.data.map((item, index) =>
      <tr key={index} className='th1' style={{ textAlign: 'left' }}>
        <td className='td1'>{item[0]}</td>
        <td className='td1'>{item[1]}</td>
        <td className='td1'>{item[2]}</td>
        <td className='td1'>{item[3]}</td>
      </tr>
    )
  return (
      <table className='table1' style={{ alignItems: 'center' }}>
        <tbody>
          <tr className='tr1'>
            <th className='th1' style={{ textAlign: 'left' }}>Title
        </th>
            <th className='th1' style={{ textAlign: 'left' }}>Artist
        </th>
            <th className='th1' style={{ textAlign: 'left' }}>Album
        </th>
            <th className='th1' style={{ textAlign: 'left' }}>Popularity
        </th>
          </tr>
          {listData}
        </tbody>
      </table>
    );

}

function ImgView(props) {
  const titles = props.title
  const artists = props.artist
  var listData = props.img_url.map((item, index) =>
  <ul class="img-item">
      <img className="albums" key={index} src={item}/>
      <div class="details">
        <h3><a class="title">{titles[index]}</a></h3>
        <p class="artist">{artists[index]}</p>
      </div>
  </ul>
  );
  return(
    <div className='row'>
      <div class='column'>{listData.slice(0,10)}</div>
      <div class='column'>{listData.slice(10,20)}</div>
      <div class='column'>{listData.slice(20,30)}</div>
      <div class='column'>{listData.slice(30,40)}</div>
      <div class='column'>{listData.slice(40,50)}</div>
    </div>
  )
}

class Top extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      table: true,
      analytics: false
  };
  }

  render() {
    const names = []
    const artists = []
    const albums = []
    const popularity = []
    const album_img = []
    const song_uri = []
    const artist_uri = []
    const items = this.props.data['data']
    for (var item in items) {
      item = items[item];
      if (item['term'] === this.props.time || this.props.time == 'saved') {
        names.push(item['title']);
        artists.push(item['artist'])
        albums.push(item['album'])
        popularity.push(item['popularity'])
        album_img.push(item['img'])
        song_uri.push(item['uri'])
        artist_uri.push(item['artist_href'])
      }
    }
    const format_data = [];
    for (let i = 0; i < names.length; i++) {
      const element = [];
      element.push(names[i]);
      element.push(artists[i]);
      element.push(albums[i]);
      element.push(popularity[i]);
      format_data.push(element);
    }

    const analysis_data = [song_uri, artist_uri];



    const display = this.state.table;
    let element;
    if(this.state.analytics){
      element = <Analytics data ={analysis_data}/>
    }
    else if(display || this.props.time == 'saved'){
      element = <Table data={format_data} /> 
    }
    else{
      element = <ImgView img_url={album_img} title={names} artist={artists} />
    }

    return (
      <div className='top'>
          <button onClick={() => this.setState({table: true, analytics:false})}>Table View</button>
          {this.props.time !== 'saved' &&
              <button onClick={() => this.setState({table: false, analytics:false})}>Img View</button>
          }
          <button onClick={() => this.setState({analytics: true})}>Analytics</button>
        <div className='topSongs'>
          {element}
        </div>
        {this.props.children}
      </div>
    );
  }

}

export default Top;
