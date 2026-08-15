#define Py_BUILD_CORE
#include <Python.h>
#include "internal/pycore_frame.h"
#include "internal/pycore_lazyimportobject.h"

static PyObject *
lazy_hook(PyObject *self, PyObject *args)
{
    PyFrameObject *frame = PyEval_GetFrame();
    if (frame == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "must be called with a frame");
        return NULL;
    }

    PyObject *callback;
    PyObject *name;
    if (!PyArg_ParseTuple(args, "OO", &callback, &name)) {
        return NULL;
    }

    PyObject *fake_builtins = PyDict_New();
    if (fake_builtins == NULL) {
        return NULL;
    }

    if (PyDict_SetItemString(fake_builtins, "__import__", callback) < 0) {
        Py_DECREF(fake_builtins);
        return NULL;
    }

    PyObject *result = _PyLazyImport_New(frame->f_frame, fake_builtins, name, NULL);
    Py_DECREF(fake_builtins);
    return result;
}

static PyMethodDef _laziness_methods[] = {
    {"lazy_hook", lazy_hook, METH_VARARGS, NULL},
    {NULL},
};

static struct PyModuleDef _laziness_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "_laziness",
    .m_size = 0,
    .m_methods = _laziness_methods,
};

PyMODINIT_FUNC
PyInit__laziness(void)
{
    return PyModuleDef_Init(&_laziness_module);
}
