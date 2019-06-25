workdir=`pwd`/../workdir

abs_workdir=`readlink -f $workdir`

pushd test-worker/
rq worker test > ${abs_workdir}/test_worker.log 2>&1 &
popd
