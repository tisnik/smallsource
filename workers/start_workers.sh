pushd test-worker/
rq worker test > test_worker.log 2>&1 &
popd
