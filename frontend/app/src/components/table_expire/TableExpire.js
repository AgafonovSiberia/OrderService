import React, {useEffect, useMemo, useState} from 'react';
import MaterialReactTable from 'material-react-table';
import axios from 'axios';


const TableExpire = () => {
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
                'http://0.0.0.0:9090/api/get_expire_orders',
            );
            setOrders(result.data);
        };
        fetchData();
    }, [count]);

  const columns = useMemo(
    () =>[{
        id: 'expire',
        header: "ИСТЕКАЮЩИЕ ЗАКАЗЫ",
        muiTableHeadCellProps: {align: 'center', sx:{fontSize: 20}},
        columns: [
            {
                accessorKey: "order_number",
                header: '№ заказа',
                size: 100
            },
            {
                accessorKey: "delivery_date",
                header: 'Дата поставки',
                size: 50
            },
        ],

    }]
  );

  return <MaterialReactTable columns={columns} data={orders} classname={"Table"}
   enableTopToolbar={false}
                             muiTableHeadCellProps={{align: 'center'}}
                             muiTableBodyCellProps={{align: 'center'}}
  />;

};

export default TableExpire;
