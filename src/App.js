import React, {Component} from 'react';
import CardsContainer from "./Components/CardsContainer.js"
import SearchCharacterForm from './Components/SearchCharacterForm'
import './App.css';

//state compent class componnet//
class App extends Component{

  state = {
    allCharacters:[],
    selectedCharacters:[],
  }

componentDidMount(){
  fetch('https://rickandmortyapi.com/api/character')
    .then(response =>response.json())
    .then(data => {
      this.setState({allCharacters: data.results})
      this.setState({selectedCharacters: data.results})

    })
}
  render(){
    return (
      <div id="app">
        <h1> Im motha fukin Rick yall!!!! </h1>
        <SearchCharacterForm/>
       <CardsContainer characters={this.state.selectedCharacters}/>
      </div>
    );
  }
}

export default App
