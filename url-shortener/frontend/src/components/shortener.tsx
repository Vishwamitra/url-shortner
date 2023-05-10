import { Fragment, useState } from "react";

function ListGroup() {

  return (
    <Fragment>
      <div className="h-100 d-flex align-items-center justify-content-center">
    <form className="form-inline">

  <div className="form-group">

    <input type="text" className="form-control" id="inputPassword2" placeholder="Full URL"/>
  </div>
  <button type="submit" className="btn btn-primary mb-2">Generate Short URL</button>
        </form>
        </div>
    </Fragment>
  );
}

export default ListGroup;
