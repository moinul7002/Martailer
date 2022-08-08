import {
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
} from "@mui/material";
import axios from "axios";
import { useEffect, useRef, useState } from "react";
import "./App.css";
import TagsPopper from "./components/popper/Popper";
import React from "react";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import ArrowDropUpIcon from "@mui/icons-material/ArrowDropUp";

function App() {
  const [getdata, updateGetData] = useState([]);
  const [filter, setFilter] = useState(false);
  const [activeModal, setActiveModal] = useState(false);
  const [activeId, setActiveId] = useState(null);
  const outerDiv = useRef();

  const handleClick = (id) => {
    if (activeId === id) {
      setActiveModal(!activeModal);
    } else {
      setActiveModal(true);
      setActiveId(id);
    }
  };

  const [search, updateSearch] = useState({ query: "", filter: "" });

  const handleSearch = (e) => {
    updateSearch({ ...search, query: e.target.value });
  };

  const onSearch = async () => {
    const res = await axios.get(
      `http://127.0.0.1:8000/api/search/?q=${search.query}&f=${search.filter}`
    );
    updateGetData(res.data.results);
  };

  useEffect(() => {
    onSearch();
  }, [search]);

  const handleFilter = () => {
    updateSearch({ ...search, filter: filter ? "ASC" : "DESC" });
    setFilter(!filter);
  };

  return (
    <div>
      <div className="list-wrapper dBlock">
        <div
          style={{
            display: "flex",
            alighItems: "center",
            marginBottom: "20px",
          }}
        >
          <div style={{ marginBottom: "10px" }}>
            <TextField
              size="small"
              id="filled-search"
              label="Search"
              type="search"
              variant="filled"
              onChange={handleSearch}
            />
          </div>
        </div>

        {getdata?.length > 0 ? (
          <div style={{ position: "relative" }}>
            <TableContainer component={Paper}>
              <Table
                sx={{ minWidth: "100%" }}
                size="small"
                aria-label="a dense table"
              >
                <TableHead>
                  <TableRow>
                    <TableCell>Video ID</TableCell>
                    <TableCell align="right">View Count</TableCell>
                    <TableCell align="right">Like Count</TableCell>
                    <TableCell align="right">Favourite Count</TableCell>
                    <TableCell align="right">Comment Count</TableCell>
                    <TableCell align="right">
                      <div
                        onClick={handleFilter}
                        style={{
                          display: "flex",
                          alightItems: "center",
                          cursor: "pointer",
                          width: "100px",
                          marginLeft: "auto",
                        }}
                      >
                        <div>Performance</div>
                        {filter === true ? (
                          <ArrowDropUpIcon />
                        ) : (
                          <ArrowDropDownIcon />
                        )}
                      </div>
                    </TableCell>
                    <TableCell align="right">Tags</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {getdata?.map((data) => (
                    <TableRow
                      key={data.vid.id}
                      sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                    >
                      <TableCell component="th" scope="row">
                        {data.vid.video_id}
                      </TableCell>
                      <TableCell align="right">{data.vid.viewCount}</TableCell>
                      <TableCell align="right">{data.vid.likeCount}</TableCell>
                      <TableCell align="right">
                        {data.vid.favoriteCount}
                      </TableCell>
                      <TableCell align="right">
                        {data.vid.commentCount}
                      </TableCell>
                      <TableCell align="right">{data.performance}</TableCell>
                      <TableCell ref={outerDiv} align="right">
                        <div>
                          <div
                            style={{ cursor: "pointer", color: "red" }}
                            onClick={() => handleClick(data.vid.id)}
                          >
                            {data.vid.id === activeId && activeModal == true ? (
                              <h4>Close</h4>
                            ) : (
                              <h4>View All</h4>
                            )}
                          </div>
                          <div
                            className={
                              data.vid.id === activeId && activeModal == true
                                ? "dBlock"
                                : "dNone"
                            }
                            style={{
                              position: "absolute",
                              background: "white",
                              zIndex: "1",
                              width: "200px",
                              right: "-250px",
                              top: "12px",
                              padding: "0px 20px 30px",
                              textAlign: "start",
                            }}
                          >
                            {" "}
                            <TagsPopper tags={data.vid.tags?.split(",")} />
                          </div>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </div>
        ) : (
          "Data Not Found."
        )}
      </div>
    </div>
  );
}

export default App;
