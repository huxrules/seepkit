#include </home/huxrules/Python3.6/Python-3.6.5/Include/Python.h>
#include </home/huxrules/SeepIntelPro/python/env/lib/python3.6/site-packages/numpy/core/include/numpy/arrayobject.h>



static PyObject * orbit_launch(PyObject *self, PyObject *args){

	
	
	//PyObject * juicebox;
	//PyObject *  trains;
	PyArrayObject * ASA; //angle start array
	PyArrayObject * AEA; //angle end array
	PyArrayObject * DSA; //depth start array
	PyArrayObject * DEA; //depth end array
	PyArrayObject * WCDA; // water column data array
	PyArrayObject * dArr; //distance array - for the output
	PyArrayObject * aArr; // angle array - for the output
	PyArrayObject * projArr; // projected array


	if (!PyArg_ParseTuple(args, "OOOOOOOO", &ASA, &AEA, &DSA, &DEA, &WCDA, &dArr, &aArr, &projArr))
		return NULL;

	npy_intp *bravo = NULL;
	bravo = PyArray_SHAPE(projArr);
	//* ok need to find the lengths of shit just in case *//

	//printf("%ld dimensions of projArr", *(npy_intp*)bravo);
	
	Py_ssize_t TupleSize = PyTuple_Size(args);
	//Py_ssize_t ListSize = PyList_Size(juicebox);

	//printf("%li tuple size\n", TupleSize);
	//printf("%li list size\n", ListSize);

	if (ASA == NULL)
	{
		printf("fuck me");
	}

	int balls = 0;
	npy_intp *wcdaShape = NULL;
	balls = PyArray_NDIM(ASA);
	//printf("%d is how many dimensions in ASA\n", balls);
	wcdaShape = PyArray_SHAPE(WCDA);
	//printf("%ld shape\n", taints[0]);
	//printf("%ld shape\n", taints[1]);
	//balls = PyArray_NDIM(WCDA);
	//printf("%d dimensions WCDA\n", balls);
	//printf("%f test 9000", WCDA[0][0])
	npy_intp *projArrShape =NULL;
	projArrShape = PyArray_SHAPE(projArr);
	//printf("%ld projArr shape\n", projArrShape[0]);
	//rintf("%ld projArr shape\n", projArrShape[1]);

	npy_intp *dArrShape =NULL;
	dArrShape = PyArray_SHAPE(dArr);
	//printf("%ld dArr shape\n", dArrShape[0]);
	//printf("%ld dArr shape\n", dArrShape[1]);

	npy_intp *aArrShape =NULL;
	aArrShape = PyArray_SHAPE(aArr);
	//rintf("%ld aArr shape\n", aArrShape[0]);
	//printf("%ld aArr shape\n", aArrShape[1]);

	npy_intp *ASAShape =NULL;
	ASAShape = PyArray_SHAPE(ASA);
	//printf("%ld ASA shape\n", ASAShape[0]);

	npy_intp *AEAShape =NULL;
	AEAShape = PyArray_SHAPE(AEA);
	//printf("%ld AEA shape\n", AEAShape[0]);

	npy_intp *DSAShape =NULL;
	DSAShape = PyArray_SHAPE(DSA);
	//printf("%ld DSA shape\n", DSAShape[0]);

	npy_intp *DEAShape =NULL;
	DEAShape = PyArray_SHAPE(DEA);
	//rintf("%ld DEA shape\n", DEAShape[0]);



	



	/// just remember this fucking numpy arrays are fucked and sideways
	

	long i = 0;
	long j = 0;
	long x = 0;
	long y = 0;
	long xcoord = 0;
	long ycoord = 0;
	double lookupDistance = 0;
	double lookupAngle = 0;
	double ASAmin = *((double*)PyArray_GETPTR1(ASA, 0));
	long ASAArrLen = (ASAShape[0]);
	//printf("ASAArrLen = %li\n",ASAArrLen);
	double AEAmax = *((double*)PyArray_GETPTR1(AEA, (ASAArrLen -1))); 
	//printf("%f %f  compare max min\n", ASAmin, AEAmax);
	
	long DSAArrLen = (DSAShape[0]);
	double DSAmin = *((double*)PyArray_GETPTR1(DSA, 0));
	double DEAmax = *((double*)PyArray_GETPTR1(DEA, (DSAArrLen -1)));
	//printf("%f %f  compare max \n", DSAmin, DEAmax);
	



	double TempStart = 0;
 	double TempEnd = 0;
 	double TempStartAlfa = 0;
 	double TempEndBeta = 0;

 	void *newStuff;
 	double dataz = 666.6;
 	double beforePoint = 0;
 	double afterPoint = 0;

	//printf("%f 0 \n",ASAmin);
	//printf("%f %ld \n",AEAmax, ASAShape[0]);
	

	for (i=0; i < projArrShape[0]; i++)
	{
		for (j=0; j<projArrShape[1]; j++)
		{
			lookupDistance = *((double*)PyArray_GETPTR2(dArr, i, j));
			//printf("%f lookupDist", lookupDistance);
			lookupAngle = *((double*)PyArray_GETPTR2(aArr, i, j));
			//printf("%f\n", lookupAngle);
			xcoord = 0;
			ycoord = 0;

			if (ASAmin >= lookupAngle && lookupAngle >= AEAmax)
			{
				//printf("made it to baller town\n");
				for (y =0; y < ASAArrLen; y++ )
				{
					TempStartAlfa = *((double*)PyArray_GETPTR1(ASA, y));
					TempEndBeta = *((double*)PyArray_GETPTR1(AEA, y));
					//printf("%f start %f end %f lookupAngle\n", TempStartAlfa, TempEndBeta, lookupAngle);
					if (TempStartAlfa > lookupAngle && lookupAngle > TempEndBeta)
					{
						//printf("found the y %li\n", y);
						ycoord = y;
						y = ASAArrLen +1;

					}
				}
			}
			else
			{
				//printf("sorry sukka\n");
			}

			if (DSAmin >= lookupDistance && lookupDistance >= DEAmax)
			{
				for (x =0; x < DSAArrLen; x++ )
				{
					TempStart = *((double*)PyArray_GETPTR1(DSA, x));
					TempEnd = *((double*)PyArray_GETPTR1(DEA, x));
					//printf("%f start %f end ", TempStart, TempEnd);
					if (TempStart > lookupDistance && lookupDistance > TempEnd)
					{
						//printf("found the x %li\n", x);
						xcoord = x;
						x = DSAArrLen + 1;

					}
				}
			}
			else
			{
				//printf("sorry sukka\n");
			}
			
			if (xcoord != 0 && ycoord != 0)
			{
			//printf("found the x,y  %li,%li\n", xcoord, ycoord);
			dataz =  *((double*)PyArray_GETPTR2(WCDA, ycoord, xcoord));
			//printf("%f dataz\n", dataz);
			newStuff =  PyArray_GETPTR2(projArr, i, j);
			beforePoint = *((double*)PyArray_GETPTR2(projArr, i, j));
			//printf("%li %li\n",i, j);
			*(double*)newStuff = dataz;
			//printf("happy horseshit %p", newStuff);
			//*newStuff = dataz;
			afterPoint =  *((double*)PyArray_GETPTR2(projArr, i, j));
			//printf("before point %f after point%f\n", beforePoint, afterPoint);

			}
		}
	}
	//printf("%ld loopz\n", i);
	//printf("%ld loopz\n", j);



	//double dataz = 666.6;


	
	//dataz =  *((double*)PyArray_GETPTR1(ASA, 0));
	//printf("%f is a sample\n", dataz);

	
	//dataz =  *((double*)PyArray_GETPTR2(WCDA, 150, 200));
	//printf("%f is a sample\n", dataz);
	//dataz =  *((double*)PyArray_GETPTR2(WCDA, 150, 201));
	//printf("%f is a sample\n", dataz);
	//dataz =  *((double*)PyArray_GETPTR2(WCDA, 150, 202));
	//printf("%f is a sample\n", dataz);
	//dataz =  *((double*)PyArray_GETPTR2(WCDA, 150, 203));
	//printf("%f is a sample\n", dataz);
	

	// Dec ref everything

	//Py_DECREF(ASA);
	//Py_DECREF(AEA);
	//Py_DECREF(DSA);
	//Py_DECREF(DEA);
	//Py_DECREF(WCDA);
	//Py_DECREF(dArr);
	//Py_DECREF(aArr);
	//Py_DECREF(projArr);

	//PyObject *copyArray;
	//copyArray = PyArray_NewCopy(projArr, NPY_CORDER);
	//copyArray = PyArray_Return(projArr);

    //Py_DECREF(ASA);
	//Py_DECREF(AEA);
	//Py_DECREF(DSA);
	//Py_DECREF(DEA);
	//Py_DECREF(WCDA);
	//Py_DECREF(dArr);
	//Py_DECREF(aArr);
	//Py_DECREF(projArr);

	//printf("ping complete\n");

	//char *s = "HTRUE";
	
	return Py_BuildValue("O", projArr);
}

static PyMethodDef AstrosMethods[] = {
	{"bats", orbit_launch, METH_VARARGS},
	{NULL,NULL}
};

static struct PyModuleDef astrosmodule = {
	PyModuleDef_HEAD_INIT,
	"astros",
	NULL,-1,
	AstrosMethods
};

PyMODINIT_FUNC PyInit_astros(void)
{
	return PyModule_Create(&astrosmodule);
}