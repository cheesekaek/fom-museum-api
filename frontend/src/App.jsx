import { BrowserRouter, Routes, Route} from 'react-router-dom'

import {Home} from './Home.jsx'
import {Sets} from './Sets.jsx'

function App() {

  return (
      <BrowserRouter>
          {/* Routes */}
          <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/wings/:wingID" element={<Sets />} />
          </Routes>
      </BrowserRouter>
  );
}



export default App
