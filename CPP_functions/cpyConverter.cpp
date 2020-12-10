#include <Python.h> // Must be first
#include <vector>
#include <stdexcept>
#include <set>
#include "cycle/find_cycle.h"
#include "fragm_alwdFaces/func.h"
#include "alpha_path/find_alpha_path.h"
#include "new_position/new_positions.h"
#include "CalculateDistances/CalculateDistances.h"

using namespace std;

// vector<int> -> List<int>
static PyObject *vectorToList_Int(const vector<int> &data) {
    PyObject *listObj = PyList_New(data.size());
    if (!listObj) {
        throw logic_error("Unable to allocate memory for Python list");
    }
    for (size_t i = 0; i < data.size(); ++i) {
        PyObject *num = PyLong_FromLong(static_cast<long>(data[i]));
        if (!num) {
            Py_DECREF(listObj);
            throw logic_error("Unable to allocate memory for Python list");
        }
        PyList_SET_ITEM(listObj, i, num);
    }
    return listObj;
}

// vector<pair<int,int>> -> List<int>
static PyObject *vectorPairToList_Int(const vector<pair<int, int>> &data) {
    PyObject *listObj = PyList_New(data.size());
    if (!listObj) {
        throw logic_error("Unable to allocate memory for Python list");
    }
    for (size_t i = 0; i < data.size(); ++i) {
        PyObject *listPair = PyList_New(2);
        PyObject *first = PyLong_FromLong(static_cast<long>(data[i].first));
        PyObject *second = PyLong_FromLong(static_cast<long>(data[i].second));
        PyList_SET_ITEM(listPair, 0, first);
        PyList_SET_ITEM(listPair, 1, second);
        PyList_SET_ITEM(listObj, i, listPair);
    }
    return listObj;
}

// list -> vector<int>
static vector<int> listToVector_Int(PyObject *incoming) {
    vector<int> data;
    if (PyList_Check(incoming)) {
        for (Py_size_t i = 0; i < PyList_Size(incoming); i++) {
            PyObject *value = PyList_GetItem(incoming, i);
            data.push_back(PyFloat_AsDouble(value));
        }
    } else {
        throw logic_error("Passed PyObject pointer is not a list or tuple!");
    }
    return data;
}

// List -> vector<pair<double, double>>
static vector<pair<double, double>> listToVectorPair_Double(PyObject *incoming) {
    vector<pair<double, double>> data;
    if (PyList_Check(incoming)) {
        for (Py_size_t i = 0; i < PyList_Size(incoming); i++) {
            PyObject *sublist = PyList_GetItem(incoming, i);
            if (PyList_Check(sublist)) {
                PyObject *first = PyList_GetItem(sublist, 0);
                PyObject *second = PyList_GetItem(sublist, 1);
                pair<double, double> subdata = {PyFloat_AsDouble(first), PyFloat_AsDouble(second)};
                date.push_back(subdata);
            }
        }
    } else {
        throw logic_error("Passed PyObject pointer is not a list or tuple!");
    }
    return data;
}

// List -> vector<pair<int, int>>
static vector<pair<int, int> > listToVectorPair_Int(PyObject *incoming) {
    vector<pair<int, int>> data;
    if (PyList_Check(incoming)) {
        for (Py_size_t i = 0; i < PyList_Size(incoming); i++) {
            PyObject *sublist = PyList_GetItem(incoming, i);
            if (PyList_Check(sublist)) {
                PyObject *first = PyList_GetItem(sublist, 0);
                PyObject *second = PyList_GetItem(sublist, 1);
                pair<int, int> subdata = {PyLong_AsLong(first), PyLong_AsLong(second)};
                data.push_back(subdata);
            }
        }
    } else {
        throw logic_error("Passed PyObject pointer is not a list or tuple!");
    }
    return data;
}

// List<List> -> vector<vector<int>>
static vector<vector<int> > listToVectorVector_Int(PyObject *incoming) {
    vector<vector<int>> data;
    if (PyList_Check(incoming)) {
        for (Py_size_t i = 0; i < PyList_Size(incoming); ++i) {
            PyObject *sublist = PyList_GetItem(incoming, i);
            if (PyList_Check(sublist)) {
                vector<int> subdata;
                for (Py_size_t j = 0; j < PyList_Size(sublist); ++j) { /
                    PyObject *value = PyList_GetItem(sublist, j);
                    subdata.push_back(PyFloat_AsDouble(value));
                }
                data.push_back(subdata);
            }
        }
    } else {
        throw logic_error("Passed PyObject pointer is not a list or tuple!");
    }
    return data;
}

static PyObject *getCycle(PyObject *self, PyObject *args) {
    PyObject *pList;
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &pList)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }
    vector<pair<int, int>> data = listToVectorPair_Int(pList);
    return vectorToList_Int(FindCycle(data));
}

static PyObject *getFragments(PyObject *self, PyObject *args) {
    PyObject *pListGraph;
    PyObject *pListSubgraph;
    if (!PyArg_ParseTuple(args, "O!O!", &PyList_Type, &pListGraph, &PyList_Type, &pListSubgraph)) {
        PyErr_SetString(PyExc_TypeError, "Passed PyObject pointer is not a list");
        return NULL;
    }
    vector<pair<int, int>> graph = listToVectorPair_Int(pListGraph);
    vector<pair<int, int>> subgraph = listToVectorPair_Int(pListSubgraph);
    vector<Fragment> fragments = GetFragments(graph, subgraph);
    PyObject *listFragments = PyList_New(fragments.size());
    for (size_t i = 0; i < fragments.size(); ++i) {
        PyObject *listMainPoints = PyList_New(fragments[i].main_points.size());
        for (size_t j = 0; j < fragments[i].main_points.size(); j++) {
            PyObject *point = PyLong_FromLong(static_cast<long>(fragments[i].main_points[j]));
            PyList_SET_ITEM(listMainPoints, j, point);
        }
        PyObject *linesList = vectorPairToList_Int(fragments[i].lines);
        PyObject *fragmentPairList = PyList_New(2);
        PyList_SET_ITEM(fragmentPairList, 0, listMainPoints);
        PyList_SET_ITEM(fragmentPairList, 1, linesList);
        PyList_SET_ITEM(listFragments, i, fragmentPairList);
    }
    return listFragments;
}

static PyObject *getAllowedFaces(PyObject *self, PyObject *args) {
    PyObject *pListMain;
    PyObject *pListFaces;
    if (!PyArg_ParseTuple(args, "O!O!", &PyList_Type, &pListMain, &PyList_Type, &pListFaces)) {
        PyErr_SetString(PyExc_TypeError, "Passed PyObject pointer is not a lis");
        return NULL;
    }
    vector<int> mainPoints = listToVector_Int(pListMain);
    vector<vector<int>> faces = listToVectorVector_Int(pListFaces);
    vector<int> allowedFaces = GetAllowedFace(mainPoints, faces);
    return vectorToList_Int(allowedFaces);
}


static PyObject *getAlphaPath(PyObject *self, PyObject *args) {
    PyObject *pListFragment;
    PyObject *pListPoints;
    if (!PyArg_ParseTuple(args, "O!O!", &PyList_Type, &pListPoints, &PyList_Type, &pListFragment)) {
        PyErr_SetString(PyExc_TypeError, "Passed PyObject pointer is not a lis");
        return NULL;
    }
    vector<pair<int, int>> fragment = listToVectorPair_Int(pListFragment);
    vector<int> mainPoints = listToVector_Int(pListPoints);
    return vectorToList_Int(FindAlphaPath(fragment, mainPoints));
}


static PyObject *newPosition(PyObject *self, PyObject *args) {
    PyObject *pListPosition;
    PyObject *pListNeighbours;
    double cool;
    double constant;
    if (!PyArg_ParseTuple(args, "O!O!dd", &PyList_Type, &pListPosition, &PyList_Type,
                          &pListNeighbours, &cool, &constant)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }
    PyObject *x = PyList_GetItem(pListPosition, 0);
    PyObject *y = PyList_GetItem(pListPosition, 1);
    pair<double, double> position = {PyFloat_AsDouble(x), PyFloat_AsDouble(y)};
    vector<pair<double, double>> neighbours = listToVectorPair_Double(pListNeighbours);
    pair<double, double> newPos = NewPosition(position, neighbours, cool, constant);
    PyObject *coordinatesList = PyList_New(2);
    PyObject *first = PyFloat_FromDouble(newPos.first);
    PyObject *second = PyFloat_FromDouble(newPos.second);
    PyList_SET_ITEM(coordinatesList, 0, first);
    PyList_SET_ITEM(coordinatesList, 1, second);
    return coordinatesList;
}

static PyObject *calculateDistances(PyObject *self, PyObject *args) {
    PyObject *pListGraph;
    PyObject *pListFace;
    double cool;
    double constant;
    if (!PyArg_ParseTuple(args, "O!O!", &PyList_Type, &pListGraph, &PyList_Type, &pListFace)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }
    vector<pair<int, int>> graph = listToVectorPair_Int(pListGraph);
    vector<int> face = listToVector_Int(pListFace);
    map<int, int> newDistances = CalculateDistances(graph, face);
    PyObject *distancesDict = PyDict_New();
    for (auto const&[key, val] : newDistances) {
        PyDict_SetItem(distancesDict, PyLong_FromLong(key), PyLong_FromLong(val));
    }
    return distancesDict;
}

static PyMethodDef myMethods[] =
        {
                {"getCycle",           (PyCFunction) getCycle,           METH_VARARGS, "returns cycle"},
                {"getFragments",       (PyCFunction) getFragments,       METH_VARARGS, "returns all fragments"},
                {"getAllowedFaces",    (PyCFunction) getAllowedFaces,    METH_VARARGS, "returns allowed faces"},
                {"getAlphaPath",       (PyCFunction) getAlphaPath,       METH_VARARGS, "returns alpha path"},
                {"newPosition",        (PyCFunction) newPosition,        METH_VARARGS, "returns new position of a point"},
                {"calculateDistances", (PyCFunction) calculateDistances, METH_VARARGS, "returns distance to outer edge for all points"},
                {NULL, NULL,                                             0, NULL}
        };

static struct PyModuleDef graphModule = {
        PyModuleDef_HEAD_INIT,
        "graphModule",
        "Module with cpp graph functions",
        -1,
        myMethods
};

PyMODINIT_FUNC PyInit_graphModule(void) {
    return PyModule_Create(&graphModule);
}