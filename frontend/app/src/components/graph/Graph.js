import React, {useEffect, useState, PureComponent} from 'react';
import axios from "axios";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Graph = () => {
    const [prices, setPrices] = useState([]);
    const [count, setCount] = useState(0);


  useEffect(() => {
    const id = setInterval(() => {
      setCount(c => c + 1); //
    }, 10000);
    return () => clearInterval(id);
  }, []);

    useEffect(() => {
        const fetchData = async () => {
            const result = await axios.get(
                'http://0.0.0.0:9090/api/price_dynamic',
            );
            setPrices(result.data);
        };
        fetchData();
    }, [count]);




return (
<LineChart
      width={900}
      height={600}
      data={prices}
      margin={{
        top: 5,
        right: 30,
        left: 20,
        bottom: 5
      }}
    >

      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" interval={0} angle={-90} fontSize={8}  />
      <YAxis dataKey="price" domain={[0, 'dataMax']} interval={0}/>
      <Tooltip />
      <Legend />

      <Line type="monotone" dataKey="price" stroke="#82ca9d" />
    </LineChart>
);



};

export default Graph;
