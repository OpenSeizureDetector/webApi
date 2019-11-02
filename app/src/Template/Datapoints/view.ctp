<?php
/**
 * @var \App\View\AppView $this
 * @var \App\Model\Entity\Datapoint $datapoint
 */
echo(print_r($datapoint));
?>
<nav class="large-3 medium-4 columns" id="actions-sidebar">
    <ul class="side-nav">
        <li class="heading"><?= __('Actions') ?></li>
        <li><?= $this->Html->link(__('Edit Datapoint'), ['action' => 'edit', $datapoint->id]) ?> </li>
        <li><?= $this->Form->postLink(__('Delete Datapoint'), ['action' => 'delete', $datapoint->id], ['confirm' => __('Are you sure you want to delete # {0}?', $datapoint->id)]) ?> </li>
        <li><?= $this->Html->link(__('List Datapoints'), ['action' => 'index']) ?> </li>
        <li><?= $this->Html->link(__('New Datapoint'), ['action' => 'add']) ?> </li>
        <li><?= $this->Html->link(__('List Users'), ['controller' => 'Users', 'action' => 'index']) ?> </li>
        <li><?= $this->Html->link(__('New User'), ['controller' => 'Users', 'action' => 'add']) ?> </li>
        <li><?= $this->Html->link(__('List Wearers'), ['controller' => 'Wearers', 'action' => 'index']) ?> </li>
        <li><?= $this->Html->link(__('New Wearer'), ['controller' => 'Wearers', 'action' => 'add']) ?> </li>
        <li><?= $this->Html->link(__('List Categories'), ['controller' => 'Categories', 'action' => 'index']) ?> </li>
        <li><?= $this->Html->link(__('New Category'), ['controller' => 'Categories', 'action' => 'add']) ?> </li>
    </ul>
</nav>
<div class="datapoints view large-9 medium-8 columns content">
    <h3><?= h($datapoint->id) ?></h3>
    <table class="vertical-table">
        <tr>
            <th scope="row"><?= __('User') ?></th>
            <td><?= $datapoint->has('user') ? $this->Html->link($datapoint->user->id, ['controller' => 'Users', 'action' => 'view', $datapoint->user->id]) : '' ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Wearer') ?></th>
            <td><?= $datapoint->has('wearer') ? $this->Html->link($datapoint->wearer->name, ['controller' => 'Wearers', 'action' => 'view', $datapoint->wearer->id]) : '' ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Category') ?></th>
            <td><?= $datapoint->has('category') ? $this->Html->link($datapoint->category->title, ['controller' => 'Categories', 'action' => 'view', $datapoint->category->id]) : '' ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Id') ?></th>
            <td><?= $this->Number->format($datapoint->id) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('AccMean') ?></th>
            <td><?= $this->Number->format($datapoint->accMean) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('AccSd') ?></th>
            <td><?= $this->Number->format($datapoint->accSd) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Hr') ?></th>
            <td><?= $this->Number->format($datapoint->hr) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('DataTime') ?></th>
            <td><?= h($datapoint->dataTime) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Created') ?></th>
            <td><?= h($datapoint->created) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Modified') ?></th>
            <td><?= h($datapoint->modified) ?></td>
        </tr>
    </table>
    <div class="row">
        <h4><?= __('DataJSON') ?></h4>
        <?= $this->Text->autoParagraph(h($datapoint->dataJSON)); ?>
    </div>
</div>
