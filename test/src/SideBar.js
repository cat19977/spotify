import React from "react";
import "./Analytics.css";
import SideNav, { Toggle, Nav, NavItem, NavIcon, NavText } from '@trendmicro/react-sidenav';
import '@trendmicro/react-sidenav/dist/react-sidenav.css';

class SideBar extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            data_type: 'genres/piechart'
        };
    }
    render(){
    return (<SideNav style={{top: 'auto', bottom: 'auto', backgroundColor:'rgba(0,0,0,0)'}}
                    onSelect={(selected) => {
                        this.props.data_type(selected)
                    }}
    >
    <SideNav.Toggle /> 
    <SideNav.Nav defaultSelected="genres/piechart" >
        <NavItem eventKey="genres">
            <NavIcon>
                <i className="genres" style={{ fontSize: '1.75em' }} />
            </NavIcon>
            <NavText>
                Top Genres
            </NavText>
            <NavItem eventKey="genres/piechart">
                    <NavText>
                    Pie Chart
                    </NavText>
                </NavItem>
                <NavItem eventKey="genres/barchart">
                    <NavText>
                        Bar Chart
                    </NavText>
                </NavItem>
        </NavItem>
        <NavItem eventKey="artists/">
            <NavIcon>
                <i className="fa fa-fw fa-line-chart" style={{ fontSize: '1.75em' }} />
            </NavIcon>
                <NavText>
                Top Artists
                </NavText>
            </NavItem>
        </SideNav.Nav>
    </SideNav> )
}
}
export default SideBar;