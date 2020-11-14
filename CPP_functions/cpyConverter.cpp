#include <Python.h> // Must be first
#include <vector>
#include <stdexcept>
#include <set>
#include "cycle/find_cycle.h"
//#include "fragm_alwdFaces"
using namespace std;

// Vector -> List
static PyObject* vectorToList_Int(const vector<int> &data) {
  PyObject* listObj = PyList_New( data.size() );
	if (!listObj) throw logic_error("Unable to allocate memory for Python list");
	for (unsigned int i = 0; i < data.size(); i++) {
		PyObject *num = PyLong_FromLong((long) data[i]);
		if (!num) {
			Py_DECREF(listObj);
			throw logic_error("Unable to allocate memory for Python list");
		}
		PyList_SET_ITEM(listObj, i, num);
	}
	return listObj;
}

// List -> Vector
static vector<int> listToVector_Int(PyObject* incoming) {
	vector<int> data;
    if (PyList_Check(incoming)) {
        for(Py_ssize_t i = 0; i < PyList_Size(incoming); i++) {
            PyObject *value = PyList_GetItem(incoming, i);
            data.push_back( PyFloat_AsDouble(value) );
        }
    } else {
        throw logic_error("Passed PyObject pointer was not a list or tuple!");
    }
	return data;
}
static vector< pair<int, int> > listToVectorPair_Int(PyObject* incoming) {
	vector<pair<int, int>> vect;
    if (PyList_Check(incoming)) {
        for(Py_ssize_t i = 0; i < PyList_Size(incoming); i++) {
            PyObject *sublist = PyList_GetItem(incoming, i);
            if (PyList_Check(sublist)) {

                PyObject *first = PyList_GetItem(sublist, 0);
                PyObject *second = PyList_GetItem(sublist, 1);
                pair<int, int> subdata = {PyLong_AsLong(first), PyLong_AsLong(second)};
            vect.push_back( subdata );
            }
        }
    } else {
        throw logic_error("Passed PyObject pointer was not a list or tuple!");
    }
	return vect;
}
// ListList -> VectorVector
static vector< vector<int> > listToVectorVector_Int(PyObject* incoming) {
	vector<vector<int>> data;

    if (PyList_Check(incoming)) {
        for(Py_ssize_t i = 0; i < PyList_Size(incoming); i++) {
            PyObject *sublist = PyList_GetItem(incoming, i);
            if (PyList_Check(sublist)) {
                vector<int> subdata;
                for(Py_ssize_t j = 0; j < PyList_Size(sublist); j++) {
                    PyObject *value = PyList_GetItem(sublist, j);
				    subdata.push_back( PyFloat_AsDouble(value) );
                }
            data.push_back( subdata );
            }
        }
    } else {
        throw logic_error("Passed PyObject pointer was not a list or tuple!");
    }
	return data;
}

static PyObject*  passListList(PyObject* self, PyObject* args)
{
    PyObject *pList;
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &pList)) {
    PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
    return NULL;
    }
    vector<vector<int>> data;
    data = listToVectorVector_Int(pList);
//    data.push_back(1);
//    data.push_back(2);
    return vectorToList_Int(data[1]);
}

static PyObject*  retVector(PyObject* self, PyObject* args)
{
    PyObject *pList;
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &pList))
    {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }
    vector<int> data;
    data = listToVector_Int(pList);
    return vectorToList_Int(data);
}

static PyObject*  getCycle(PyObject* self, PyObject* args)
{
    PyObject *pList;
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &pList))
    {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }
    vector< pair<int, int> > data = listToVectorPair_Int(pList);
    return vectorToList_Int(FindCycle(data));
}

static PyMethodDef myMethods[] =
{
    {"retVector", (PyCFunction)retVector, METH_VARARGS, "returns list from vector"},
    {"passListList", (PyCFunction)passListList, METH_VARARGS, "returns list list from vector vector"},
    {"getCycle", (PyCFunction)getCycle, METH_VARARGS, "returns cycle"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef graphModule = {
	PyModuleDef_HEAD_INIT,
	"graphModule",
	"Module with cpp graph functions",
	-1,
	myMethods
};

PyMODINIT_FUNC PyInit_graphModule(void)
{
    return PyModule_Create(&graphModule);
}