import React, {Component} from 'react';
import CardsContainer from "./Components/CardsContainer.js"
import SearchCharacterForm from './Components/SearchCharacterForm'
import './App.css';

//state compent class componnet//
class App extends Component{

  state = {
    allCharacters:[],
    selectedCharacters:[],
    inputValue:""
  }

componentDidMount(){
  fetch('https://rickandmortyapi.com/api/character')
    .then(response =>response.json())
    .then(data => {
      this.setState({allCharacters: data.results})
      this.setState({selectedCharacters: data.results})

    })
}

filterCharacters = (event ) => {
  const input = event.target.value
  const filterCharacters = this.state.allCharacters
    .filter(
      character => (
        character.name
        .toLowerCase()
        .includes(input.toLowerCase())
      )
    )
}
  render(){
    return (
      <div id="app">
        <h1> Im motha fukin Rick yall!!!! </h1>
        <SearchCharacterForm filterCharacters={this.filterCharacters}/>
       <CardsContainer characters={this.state.selectedCharacters}/>
      </div>
    );
  }
}

export default App
