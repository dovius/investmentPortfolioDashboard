import React, { useState, useEffect } from 'react';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import Container from '@mui/material/Container';


function createData(name, timestamp, price, change, changeProd) {
  return { name, timestamp, price, change, changeProd };
}

function formatDecimal(decimal) {
  return (Math.round(decimal * 100) / 100).toFixed(4)
}

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/summary').then(res => res.json()).then(data => {
      let rows = []
      data.map((entry) => {
        rows.push(createData(entry.name, entry.priceNew.timestamp, formatDecimal(entry.priceNew.price), formatDecimal(entry.priceChange), formatDecimal(entry.priceChangeProc)))
      })
      setData(rows)
    });
    
  }, []);

  return (
    <Container maxWidth="lg">
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell align="right">Last update</TableCell>
            <TableCell align="right">Price</TableCell>
            <TableCell align="right">Change</TableCell>
            <TableCell align="right">Change %</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row) => (
            <TableRow
              key={row.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.name}
              </TableCell>
              <TableCell align="right">{row.timestamp}</TableCell>
              <TableCell align="right">{row.price}</TableCell>
              <TableCell align="right" sx={{color: row.change > 0 ? 'green' : 'red'}}>{row.change}</TableCell>
              <TableCell align="right" sx={{color: row.change > 0 ? 'green' : 'red'}}>{row.changeProd} %</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
    </Container>
  );
}

export default App;
