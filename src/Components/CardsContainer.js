import React from 'react'
import Card from './Card'

export default function CardsContainer( {characters} ){
    return(
        <section id="cards-container">
        {
            characters
                .map( character => (
                <Card character ={character}/>
        ))
        }      
        </section>
    )
}
