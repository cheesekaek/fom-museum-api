import {Link} from 'react-router-dom'
import archaeology from './assets/archaeology.png'
import fish from './assets/fish.png'
import flora from './assets/flora.png'
import insects from './assets/insects.png'
import {useEffect, useState} from "react";
import "./style.css"

export function Home() {
    // get data
    const [wings, setWings] = useState([]);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/wings")
            .then(res => res.json())
            .then(data => setWings(data))
    }, []);

    const wingsImg = {
        // images
        "Archaeology": archaeology,
        "Fish": fish,
        "Flora": flora,
        "Insects": insects
    }

    return (
        <div>
            <h1 className="title">Fields of Mistria Museum Tracker</h1>
            <div className="wings-container">
                {wings.map((wing) =>
                    <Link key={wing.id} to={`/wings/${wing.id}`}>
                        <button
                            style={{backgroundColor: "transparent", borderColor: "transparent"}}>
                            <img src={wingsImg[wing.name]} alt={wing.name}/>
                            <p>{wing.name} Wing</p>
                        </button>
                    </Link>
                )}
            </div>
        </div>
    )
}