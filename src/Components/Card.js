import React from 'react'

export default function card({ character }){
    return(
        <div className ="card">
                    <img src={character.image}/>
                <h3>{character.name}</h3>) 
                </div>
    )
}