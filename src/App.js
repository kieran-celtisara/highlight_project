import { useState } from "react";

export default function MergePlayer() {
  const [videoReady, setVideoReady] = useState(false);
  const [players, setPlayers] = useState([]);
  const mergeClips = async () => {
    const res = await fetch("http://127.0.0.1:8000/merge", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(players),
    });

    const data = await res.json();
    if (data?.message === "Merged successfully") {
      console.log('merge work')
      setVideoReady(true); // Tell React the video is ready to show
    }
  };
  const testPlayers = [
    "Brock Purdy",
    "Isaac Guerendo",
    "Ricky Pearsall",
    "Deebo Samuel",
    "Jared Goff",
    "Jameson Williams",
    "Amon-Ra St. Brown",
    "Jahmyr Gibbs",
    "Sam Laporta",
  ];
  console.log(players.includes("Jahmyr Gibbs"));
  return (
    <div>
      <div style={{ display: "flex" }}>
        {testPlayers.map((item) => (
          <div>
            <button onClick={() => setPlayers((prev) => [...prev, item])}>
              {item}
            </button>
            {players.includes(item) && <div>selected</div>}
          </div>
        ))}
      </div>
      <button onClick={mergeClips}>Merge Clips</button>

      {videoReady && (
        <video width="640" height="360" controls>
          <source src="http://127.0.0.1:8000/video" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      )}
    </div>
  );
}
