import React, {useEffect, useMemo, useState} from 'react';
import MaterialReactTable from 'material-react-table';
import axios from 'axios';


const Table = () => {
    const [orders, setOrders] = useState([]);
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
                'http://0.0.0.0:9090/api/orders',
            );
            setOrders(result.data);
        };
        fetchData();
    }, [count]);

  const columns = useMemo(
    () => [
      {
        accessorKey: "id",
        header: '№',
           size: 10
      },
      {
        accessorKey: "order_number",
        header: '№ заказа',
           size: 100
      },
      {
        accessorKey: "price_in_dollars",
        header: 'Стоимость в USD',
          size: 50
      },
      {
        accessorKey: "price_in_rubles",
        header: 'Стоимость в RUB',
           size: 80,
      },
      {
        accessorKey: "delivery_date",
        header: 'Дата поставки',
           size: 50
      },
    ],
    [],
  );

  return <MaterialReactTable columns={columns} data={orders} classname={"Table"} />;

};

export default Table;
