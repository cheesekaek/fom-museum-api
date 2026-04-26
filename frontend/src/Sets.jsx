import {useParams} from 'react-router-dom'
import {useEffect, useState} from "react";
import "./style.css"

export function Sets() {
    const { wingID } = useParams();
    const [wing, setWing] = useState()

    // data
    useEffect(() => {
        fetch(`http://127.0.0.1:8000/wings/${wingID}`)
            .then(res => res.json())
            .then(data => setWing(data))
    }, [wingID]);

    if (!wing) return <div>...</div>;

    return (
        <div className="sets-page">
            <h1 className="wing-title">{wing.name} Wing</h1>

            {wing.sets?.map(set =>
                <SetTable key={set.id} wingName={wing.name} set={set} />
            )}
        </div>
    )
}

const wingColumns = {
    // specific columns for each wing (not including the common columns across all)
    Fish: ["locations", "weather", "rarity", "size"],
    Insects: ["locations", "seasons", "time", "weather", "rarity"],
    Flora: ["sources", "locations"],
    Archaeology: ["locations", "rarity"],
};

function SetTable({ set, wingName }) {
    const columns = wingColumns[wingName] || [];

    return (
        <div>
            <h3 className="set-title">{set.name}</h3>

            <table>
                <thead>
                    <tr>
                        <th>Completed</th>
                        <th>Image</th>
                        <th>Name</th>
                        {columns.map(col =>
                        <th key={col}>{col}</th>)}
                    </tr>
                </thead>
                <tbody>
                {set.items?.map(item =>
                    <ItemRow key={item.id} item={item} columns={columns}/>
                )}
                </tbody>
            </table>
        </div>
    )
}


function ItemRow( {item, columns }) {
    const [isChecked, setIsChecked] = useState(item.completed)

    const onHandleChange = async () => {
        const toggle = !isChecked // since setIsChecked is async, we can't use isChecked directly
        setIsChecked(!isChecked)

        try {
            const res = await fetch(`http://127.0.0.1:8000/items/${item.id}`,
                {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        completed: toggle
                    })
                });
        } catch (error) {
            setIsChecked(!toggle)
            console.error(error)
        }
    };

    return (
        <tr>
            <td>
                <input type="checkbox" checked={isChecked}
                       onChange={onHandleChange}
                />
            </td>
            <td>
                <img src={`/${item.img}`} width="40"  alt={item.name}/>
            </td>
            <td>{item.name}</td>
            {columns.map(col =>
                <td key={col}>
                    {Array.isArray(item[col]) ? item[col]?.join(", ") : item[col] ?? ""}
                </td>
            )}
        </tr>
    )
}