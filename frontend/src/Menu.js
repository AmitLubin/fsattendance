import { Component } from "react";
import "./css/Menu.css"
import Searches from "./Searches";
import Category from "./Category";

class Menu extends Component {
    dropDownEventLoader(){
        let checkList = document.getElementById('ddcbl');
        checkList.getElementsByClassName('anchor')[0].onclick = function(evt) {
            if (checkList.classList.contains('visible'))
                checkList.classList.remove('visible');
            else
                checkList.classList.add('visible');     
        }
    }

    checkBoxesEventsLoader(){
        const checkBoxes = {
            roomName: document.getElementById('check-room-name'),
            roomStart: document.getElementById('check-room-start'),
            roomFinish: document.getElementById('check-room-end'),
            studentName: document.getElementById('check-student-name'),
            studentMail: document.getElementById('check-student-mail'),
            studentTime: document.getElementById('check-student-time'),
            studentOverall: document.getElementById('check-student-overall'),
            studentPlatform: document.getElementById('check-student-platform')
        };

        const allCategories = document.getElementById('check-all');
        allCategories.checked = true;

        allCategories.onclick = function(e){
            if (allCategories.checked){
                for (const [key, element] of Object.entries(checkBoxes))
                    element.checked = false;
            } else if (!allCategories.checked){
                for (const [key, element] of Object.entries(checkBoxes))
                    element.checked = true;
            }
        }

        for (const [key, element] of Object.entries(checkBoxes)){
            element.onclick = function(e){
                if (element.checked)
                    allCategories.checked = false;
                else if (!element.checked){
                    let flag = false;
                    for (const [key, element] of Object.entries(checkBoxes))
                        if (element.checked)
                            flag = true;
                    if (!flag)
                        allCategories.checked = true;
                }
            }
        }
    }

    state = { Categories: ["*"] }

    constructor(){
        super();
    }

    componentDidMount(){
        this.dropDownEventLoader();
        this.checkBoxesEventsLoader();
    }
    
    render(){
        return(
            <div className="topnav">
                <div className="menu-item">
                    <Category />
                </div>
                <div className="menu-item">
                    <Searches />
                </div>
            </div> 
        );
    }
}

export default Menu;