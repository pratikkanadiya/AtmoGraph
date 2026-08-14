import SupplyChainGraph from "./components/SupplyChainGraph";

function App() {
  return (
    <div>
      <header>
        <h1>AtmoGraph</h1>
        <p>Supply Chain Ripple Effect Predictor</p>
      </header>

      <main>
        <h2>Global Supply Chain Network</h2>

        <SupplyChainGraph />
      </main>
    </div>
  );
}

export default App;