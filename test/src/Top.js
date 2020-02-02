import React from "react";
import "./top.css";

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
    <div class='item'>
      <img className="albums" key={index} src={item}/>
      <span class="title">{titles[index]}</span>
      <span class="artist">{artists[index]}</span>
    </div>
    );
  return(
    <div className='column'>
      <div class='flex-container'>{listData.slice(0,10)}</div>
      <div class='flex-container'>{listData.slice(10,20)}</div>
      <div class='flex-container'>{listData.slice(20,30)}</div>
      <div class='flex-container'>{listData.slice(30,40)}</div>
      <div class='flex-container'>{listData.slice(40,50)}</div>
    </div>
  )
}

class Top extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      names: [],
      artists: [],
      albums: [],
      popularity: [],
      album_img: [],
      data: [],
      table: true
    };
    this.set_initial_data = this.set_initial_data.bind(this);
  }

  componentDidUpdate(prevProps) {
    console.log(this.props.time)
    if (this.props.time !== prevProps.time) {
      this.set_initial_data(this.props.data, this.props.time);
    }
  }
  set_initial_data(data, time) {
    const names = []
    const artists = []
    const albums = []
    const popularity = []
    const album_img = []
    var items = data['data'];
    for (var item in items) {
      item = items[item];
      if (item['term'] == time) {
        names.push(item['title']);
        artists.push(item['artist'])
        albums.push(item['album'])
        popularity.push(item['popularity'])
        album_img.push(item['img'])
      }
    }
    const format_data = [];
    for (let i = 0; i < this.state.names.length; i++) {
      const element = [];
      element.push(names[i]);
      element.push(artists[i]);
      element.push(albums[i]);
      element.push(popularity[i]);
      format_data.push(element);
    }
    this.setState({
      names: names,
      artists: artists,
      albums: albums,
      popularity: popularity,
      data: format_data,
      album_img: album_img
    });
  }

  render() {
    const display = this.state.table;
    const data_state = this.state.data;
    const img_url = this.state.album_img;
    console.log(img_url);
    let element;
    if(display){
      element = <Table data={data_state} /> 
    }
    else{
      element = <ImgView img_url={img_url} title={this.state.names} artist={this.state.artists} />
    }

    return (
      <div className='top'>
        <button onClick={() => this.setState({table: true})}>Table View</button>
        <button onClick={() => this.setState({table: false})}>Img View</button>
        <div className='topSongs'>
          {element}
        </div>
        {this.props.children}
      </div>
    );
  }

}

export default Top;
