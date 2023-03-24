import './App.css';
import React from 'react';
import FullWidthGrid from './components/grid/Grid'
import Logo from './components/logo/Logo'
import Graph from './components/graph/Graph'
function App() {
  return (
      <React.StrictMode>
      <Logo />
      <FullWidthGrid />
      </React.StrictMode>);
}

export default App;
