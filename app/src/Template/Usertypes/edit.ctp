<?php
/**
 * @var \App\View\AppView $this
 * @var \Cake\Datasource\EntityInterface $usertype
 */
?>
<nav class="large-3 medium-4 columns" id="actions-sidebar">
    <ul class="side-nav">
        <li class="heading"><?= __('Actions') ?></li>
        <li><?= $this->Form->postLink(
                __('Delete'),
                ['action' => 'delete', $usertype->id],
                ['confirm' => __('Are you sure you want to delete # {0}?', $usertype->id)]
            )
        ?></li>
        <li><?= $this->Html->link(__('List Usertypes'), ['action' => 'index']) ?></li>
    </ul>
</nav>
<div class="usertypes form large-9 medium-8 columns content">
    <?= $this->Form->create($usertype) ?>
    <fieldset>
        <legend><?= __('Edit Usertype') ?></legend>
        <?php
            echo $this->Form->control('title');
            echo $this->Form->control('description');
        ?>
    </fieldset>
    <?= $this->Form->button(__('Submit')) ?>
    <?= $this->Form->end() ?>
</div>
