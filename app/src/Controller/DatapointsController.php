<?php
// src/Controller/DatapointsController.php

namespace App\Controller;

use Cake\Event\Event;


class DatapointsController extends AppController
{
    // Disable csrf protection for the add event as this does not work for ajax calls.
    // from https://stackoverflow.com/questions/51508171/csrf-token-in-cakephp-when-doing-a-curl-post-request/51959878#51959878
    public function beforeFilter(Event $event)
    {	
        parent::beforeFilter($event);
        //$this->Authentication->allowUnauthenticated(['index']);
        $result = $this->Authentication->getResult();
        if (!$result->isValid()) {
            //echo "beforeFilter(): Authentication failed\n";
            //print_r($result->getData());
            //print_r($result->getErrors());
            $response = $this->response->withStatus(403);
            return $response;            
        }
        else {
            //echo("beforeFilter - Authenticated OK");
        }
    }

    public function index()
    {
        $this->loadComponent('Paginator');
        $user = $this->request->getAttribute('identity');
        $query = $user->applyScope('index', $this->Datapoints->find());
        $datapoints = $this->Paginator->paginate($query);
        
        $this->set(compact('datapoints'));
        $this->set('_serialize', ['datapoints']);
    }

    public function view($id)
    {   
        $datapoint = $this->Datapoints->get($id);
        $this->Authorization->authorize($datapoint);
 

        $this->set(compact('datapoint'));
        $this->set('_serialize', ['datapoint']);
    }

    public function add()
    {
        $msg = "";
        $datapoint = "";
        $this->request->allowMethod(['post', 'put']);
        $data = $this->request->getData();

        //$datapoint = $this->Datapoints->addDatapoint($data);
        $datapoint = $this->Datapoints->newEntity();

        // Check the user is authorised to create datapoints
        $this->Authorization->authorize($datapoint,'create');

        // Check that the authenticated user is allowed to add data for the
        // specified wearer.
        $userId = $this->Authentication->getIdentity()->getIdentifier();
        $wearerId = $data['wearerId'];
        if (!$this->Datapoints->isValidWearer($userId, $wearerId)) {
            debug("Invalid wearerId ".$wearerId." for this user(".$userId.")",false);
            $msg = "Invalid wearer id (".$wearerId.") for the authenticated user";
            $this->set([
                'msg' => $msg,
                'datapoint' => $datapoint,
                #'data' => $data,
                '_serialize' => ['msg', 'datapoint']
            ]);
            $this->setResponse($this->response->withStatus(403) );
            return $this->response; 
        }
                
        
        $patchdata = array();
        $patchdata['user_id'] = $userId;
        $patchdata['wearer_id'] = $wearerId;
        $patchdata['dataJSON'] = json_encode($data);
        $patchdata['dataTime'] = date('Y-m-d H:i:s', strtotime($data['dateStr'])); 
        
        // Calculate the average acceleration over the datapoint period
        $accSum = 0.0;
        $nData = 0;
        if (count($data['rawData'])>0) {
            foreach ($data['rawData'] as $val) {
        	    $accSum += $val;
                $nData += 1;
            }
        }
        if ($nData<>0) {
            $accMean = $accSum/$nData;
        } else {
            $accMean = 0.;
        }
        $patchdata['accMean'] = $accMean;
        
        // ...then the standard deviation of the acceleration data.
        $devSq = 0;
        foreach ($data['rawData'] as $val) {
            $devSq += pow($val - $accMean, 2);
        }
        if ($nData<>0) {
            $patchdata['accSd'] = (float)sqrt($devSq/$nData);
        } else {
            $patchdata['accSd'] = 0.0;
        }
        $patchdata['hr'] = $data['hr'];
        
        //debug($patchdata,false);
        $datapoint = $this->Datapoints->patchEntity($datapoint, $patchdata);
        
        if ($this->Datapoints->save($datapoint)) {
            $msg="Success";
        } else {
            $msg="Failed";
        }
        
        $this->set([
            'msg' => $msg,
            'datapoint' => $datapoint,
            '_serialize' => ['msg', 'datapoint']
        ]);
    }
    
    public function edit($id) {
        $datapoint = $this->Datapoints->get($id);
        $this->Authorization->authorize($datapoint);
        $this->Datapoints->patchEntity($datapoint, $this->request->getData());
        
        if ($this->Datapoints->save($datapoint)) {
            $msg="Success";
        } else {
            $msg="Failed";
        }
        $this->set([
            'msg' => $msg,
            'datapoint' => $datapoint,
            '_serialize' => ['msg', 'datapoint']
        ]);
        $this->set('_serialize', ['msg']);
    }


    public function setCategory($id,$cat)
    {
	$datapoint = $this->Datapoints->get($id);
    $this->Authorization->authorize($datapoint);
	$datapoint->category_id = $cat;
	if ($this->Datapoints->save($datapoint)) {
	   $msg="Success";
	} else {
	  $msg="Failed";
	}
    	$this->set(compact('msg'));
	$this->set('_serialize', ['msg']);
    }
}