import { Component } from "react";
import './css/App.css';
import Menu from "./Menu";
import Table from "./Table";

class App extends Component {
    state = { data: [], categories: {
        roomName: true,
        roomStart: true,
        roomFinish: true,
        studentName: true,
        studentMail: true,
        studentTimeIntervals: true,
        studentOverallTime: true,
        studentPlatform: true
    }};
    
    constructor(){
        super();
    }

    changeState = (newDataValue, allCategories, newCategoriesValue) => {
        this.setState({ data: newDataValue, categories: {
            roomName: allCategories || newCategoriesValue.room_name,
            roomStart: allCategories || newCategoriesValue.room_start,
            roomFinish: allCategories || newCategoriesValue.room_finish,
            studentName: allCategories || newCategoriesValue.name,
            studentMail: allCategories || newCategoriesValue.email,
            studentTimeIntervals: allCategories || newCategoriesValue.time,
            studentOverallTime: allCategories || newCategoriesValue.overall_time,
            studentPlatform: allCategories || newCategoriesValue.platform
        }});
    }

    async componentDidMount(){
        await fetch('http://localhost:5000/')
            .then(res => res.json())
            .then(newData => {;
                this.setState({ data: newData.results });
        });
    }
    
    render() {
        console.log(this.state)

        return(
            <div className="background">
                <div className="menu">
                    <Menu changeState={this.changeState}/>
                </div>
            </div>
        );
    }
    
}

export default App;

/*
                <div className="list">
                    <div className="table">
                        <table>
                            <thead id="thead">
                                <tr>
                                    <th className="cell">Room name</th>
                                    <th className="cell">Room start time</th>
                                    <th className="cell">Room end time</th>
                                    <th className="nameCell">Student name</th>
                                    <th className="mailCell">Student mail</th>
                                    <th className="cell">Student attendance time stamps</th>
                                    <th className="cell">Student overall attendance time (mins)</th>
                                    <th className="cell">Student platform</th>
                                </tr>
                            </thead>
                            <tbody id="tbody">
                                <Table queries={this.state.data}/>
                            </tbody>
                        </table>  
                    </div>
                </div>
*/