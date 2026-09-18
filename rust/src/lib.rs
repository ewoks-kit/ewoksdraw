use org_eclipse_elk_graph_json::org::eclipse::elk::graph::json::layout_api;
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;


#[pyfunction]
#[pyo3(signature = (graph_json, options_json = "{}"))]
fn layout_json(graph_json: &str, options_json: &str) -> PyResult<String> {
    layout_api::layout_json(graph_json, options_json).map_err(PyRuntimeError::new_err)
}

#[pymodule]
fn _elk_rs(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(layout_json, module)?)?;
    Ok(())
}
