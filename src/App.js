import React, {Component} from 'react';
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
        
      </div>
    )
  }
}

export default App
