import * as React from "react";
import Box from "@mui/material/Box";
import Popper from "@mui/material/Popper";
import Button from "@mui/material/Button";
import Fade from "@mui/material/Fade";
import Paper from "@mui/material/Paper";

export default function TagsPopper({ tags }) {
  // const [anchorEl, setAnchorEl] = React.useState(null);
  // const [open, setOpen] = React.useState(false);
  // const [placement, setPlacement] = React.useState();

  // const handleClick = (newPlacement) => (event) => {
  //   setAnchorEl(event.currentTarget);
  //   setOpen((prev) => placement !== newPlacement || !prev);
  //   setPlacement(newPlacement);
  // };

  // console.log(open);

  return (
    <div style={{ listStyle: "none" }}>
      {tags?.map((li) => (
        <li key={li}>{li}</li>
      ))}
    </div>
  );
}
