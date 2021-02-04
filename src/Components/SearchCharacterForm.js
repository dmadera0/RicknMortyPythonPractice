import React from 'react'

export default function SearchCharacterFrom({filterCharacters}){
    return(
        <form>
            <label>Search Character by Name: </label>
            <input type= "text" onChange={ filterCharacters }></input>
        </form>
    )
}