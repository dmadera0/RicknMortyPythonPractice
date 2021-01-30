import React from 'react'

export default function CardsContainer( {characters} ){
    return(
        <section id="cards-container">
        {
            characters
                .map( character => (
                <div className ="card">
                    <img src={character.image}/>
                <h3>{character.name}</h3>) 
                </div>
        ))
        }      
        </section>
    )
}
