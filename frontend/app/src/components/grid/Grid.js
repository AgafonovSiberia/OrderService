import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Unstable_Grid2';

import Table from '../table/Table'
import Graph from '../graph/Graph'
import TableTotal from '../table_total/TableTotal'

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

export default function FullWidthGrid() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid xs={10} md={7}>
          <Item><Table /></Item>
        </Grid>
          <Grid xs={10} md={5}>
          <Item><TableTotal /></Item>
        </Grid>
        <Grid xs={10} md={7}>
          <Item><Graph /></Item>
        </Grid>


      </Grid>
    </Box>
  );
}

