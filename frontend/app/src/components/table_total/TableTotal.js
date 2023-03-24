import React, {useEffect, useMemo, useState} from 'react';
import MaterialReactTable from 'material-react-table';
import axios from 'axios';


const TableTotal = () => {
    const [totals, setTotals] = useState([]);
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
                'http://0.0.0.0:9090/api/total',
            );
            setTotals(result.data);
        };
        fetchData();
    }, [count]);

  const columns = useMemo(
    () => [
      {
        accessorKey: "total_sum_in_dollars",
        header: 'Сумма в долларах',
           size: 50
      },
      {
        accessorKey: "total_sum_in_rubles",
        header: 'Сумма в рублях',
           size: 50
      }
    ],
    [],
  );

  return <MaterialReactTable columns={columns} data={totals} classname={"Table"}
                             enableColumnActions={false}
      enableColumnFilters={false}
      enablePagination={false}
      enableSorting={false}
      enableBottomToolbar={false}
      enableTopToolbar={false}
                             muiTableHeadCellProps={{align: 'center',
                 sx: {
                fontWeight: 'normal',
                fontSize: '24px',
                }
  }
  }
                             muiTableBodyCellProps={{align: 'center',
                 sx: {
                fontWeight: 'bold',
                fontSize: '24px',
                }
  }}

      muiTableBodyRowProps={{ hover: false }}/>;

};

export default TableTotal;
